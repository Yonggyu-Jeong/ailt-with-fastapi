from fastapi import FastAPI, HTTPException, Depends, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import torch
from PIL import Image
from io import BytesIO
import base64
import diffusers
import uvicorn
import json

router_image = APIRouter()


class Config:
    def __init__(self, hf_token, custom_models):
        self.hf_token = hf_token
        self.custom_models = custom_models


def get_config():
    try:
        config_file = open('config.json', 'r')
        config_data = json.loads(config_file.read())
        return Config(hf_token=config_data.get('hf_token'), custom_models=config_data.get('custom_models', []))
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="config.json not found.")


def get_manager(config: Config = Depends(get_config)):
    manager = EngineManager()
    manager.add_engine('txt2img', EngineStableDiffusion(diffusers.StableDiffusionPipeline, config, sibling=None))
    manager.add_engine('img2img', EngineStableDiffusion(diffusers.StableDiffusionImg2ImgPipeline,
                                                        config, sibling=manager.get_engine('txt2img')))
    manager.add_engine('masking', EngineStableDiffusion(diffusers.StableDiffusionInpaintPipeline,
                                                        config, sibling=manager.get_engine('txt2img')))
    for custom_model in config.custom_models:
        manager.add_engine(custom_model['url_path'],
                           EngineStableDiffusion(diffusers.StableDiffusionPipeline, config,
                                                 sibling=manager.get_engine('txt2img'),
                                                 custom_model_path=custom_model['model_path'],
                                                 requires_safety_checker=custom_model['requires_safety_checker']))
    return manager


class TaskParams(BaseModel):
    seed: int = 0
    num_outputs: int = 1
    prompt: str = None
    init_image: UploadFile = None
    mask_image: UploadFile = None
    num_inference_steps: int = 100
    guidance_scale: float = 7.5
    eta: float = 0.0
    width: int = 512
    height: int = 512
    strength: float = 0.7


def pil_to_b64(input):
    buffer = BytesIO()
    input.save(buffer, 'PNG')
    output = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    buffer.close()
    return output


def b64_to_pil(input):
    output = Image.open(BytesIO(base64.b64decode(input)))
    return output


def get_compute_platform(context):
    try:
        import torch
        if torch.cuda.is_available():
            return 'cuda'
        else:
            return 'cpu'
    except ImportError:
        return 'cpu'


class Engine(object):
    def __init__(self):
        pass

    def process(self, kwargs):
        return []


class EngineStableDiffusion(Engine):
    def __init__(self, pipe, config, sibling=None, custom_model_path=None, requires_safety_checker=True):
        super().__init__()
        if sibling is None:
            self.engine = pipe.from_pretrained('runwayml/stable-diffusion-v1-5', use_auth_token=config.hf_token.strip())
        elif custom_model_path:
            if requires_safety_checker:
                self.engine = diffusers.StableDiffusionPipeline.from_pretrained(custom_model_path,
                                                                                safety_checker=sibling.engine.safety_checker,
                                                                                feature_extractor=sibling.engine.feature_extractor)
            else:
                self.engine = diffusers.StableDiffusionPipeline.from_pretrained(custom_model_path,
                                                                                feature_extractor=sibling.engine.feature_extractor)
        else:
            self.engine = pipe(
                vae=sibling.engine.vae,
                text_encoder=sibling.engine.text_encoder,
                tokenizer=sibling.engine.tokenizer,
                unet=sibling.engine.unet,
                scheduler=sibling.engine.scheduler,
                safety_checker=sibling.engine.safety_checker,
                feature_extractor=sibling.engine.feature_extractor
            )
        self.engine.to(get_compute_platform('engine'))

    def process(self, kwargs):
        output = self.engine(**kwargs)
        return {'image': output.images[0], 'nsfw': output.nsfw_content_detected[0]}


class EngineManager(object):
    def __init__(self):
        self.engines = {}

    def has_engine(self, name):
        return name in self.engines

    def add_engine(self, name, engine):
        if self.has_engine(name):
            return False
        self.engines[name] = engine
        return True

    def get_engine(self, name):
        if not self.has_engine(name):
            return None
        engine = self.engines[name]
        return engine


@router_image.get('/')
def root():
    return {"message": "Hello World"}


@router_image.get('/home')
def home():
    return {"message": "Hello World"}


@router_image.get('/ping')
async def stable_ping():
    return JSONResponse(content={'status': 'success'})


@router_image.get('/custom_models')
async def stable_custom_models(config: Config = Depends(get_config)):
    if config.custom_models is None:
        return JSONResponse(content=[])
    else:
        return JSONResponse(content=config.custom_models)


@router_image.post('/txt2img')
async def stable_txt2img(params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await _generate('txt2img', params, manager)


@router_image.post('/img2img')
async def stable_img2img(params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await _generate('img2img', params, manager)


@router_image.post('/masking')
async def stable_masking(params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await _generate('masking', params, manager)


@router_image.post('/custom/{model}')
async def stable_custom(model: str, params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await _generate('txt2img', params, manager, model)


async def _generate(task: str, params: TaskParams, manager: EngineManager, model: str = None):
    engine = manager.get_engine(task)
    output_data = {}

    try:
        total_results = []
        for i in range(params.num_outputs):
            new_seed = params.seed if params.seed == 0 else torch.Generator(
                device=get_compute_platform('generator')).manual_seed(params.seed).seed()
            args_dict = {
                'prompt': [params.prompt] if params.prompt else None,
                'num_inference_steps': params.num_inference_steps,
                'guidance_scale': params.guidance_scale,
                'eta': params.eta,
                'generator': torch.Generator(device=get_compute_platform('generator')),
            }
            if task == 'txt2img':
                args_dict['width'] = params.width
                args_dict['height'] = params.height
            if task == 'img2img' or task == 'masking':
                init_img_pil = b64_to_pil(params.init_image.file.read()) if params.init_image else None
                args_dict['init_image'] = init_img_pil
                args_dict['strength'] = params.strength
            if task == 'masking':
                mask_img_pil = b64_to_pil(params.mask_image.file.read()) if params.mask_image else None
                args_dict['mask_image'] = mask_img_pil

            pipeline_output = engine.process(args_dict)
            pipeline_output['seed'] = new_seed
            total_results.append(pipeline_output)

        output_data['status'] = 'success'
        images = []
        for result in total_results:
            images.append({
                'base64': pil_to_b64(result['image'].convert('RGB')),
                'seed': result['seed'],
                'mime_type': 'image/png',
                'nsfw': result['nsfw']
            })
        output_data['images'] = images
    except RuntimeError as e:
        output_data['status'] = 'failure'
        output_data[
            'message'] = 'A RuntimeError occurred. You probably ran out of GPU memory. Check the server logs for more details.'
        print(str(e))
        raise HTTPException(status_code=500, detail=output_data)

    return JSONResponse(content=output_data)


config = get_config()
manager = get_manager(config)