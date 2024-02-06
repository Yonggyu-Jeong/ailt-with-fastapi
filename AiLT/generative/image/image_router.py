from generative.image.image_def import get_img_config, get_manager

#router_image = APIRouter()

#TODO config와 taskParam은 요청시 마다 가변돼야함.
engine_config = get_img_config()
engine_manager = get_manager(engine_config)

"""

@router_image.get('/')
def image_home():
    return {"message": "Hello World"}


@router_image.get('/custom_models')
async def stable_custom_models(config: ImgConfig = Depends(get_img_config)):
    if config.custom_models is None:
        return JSONResponse(content=[])
    else:
        return JSONResponse(content=config.custom_models)



@router_image.post('/txt2img')
async def stable_txt2img(params: TaskParams = Depends(), manager: EngineManager = Depends(engine_manager)):
    return await dream('txt2img', params, manager)


@router_image.post('/img2img')
async def stable_img2img(params: TaskParams = Depends(), manager: EngineManager = Depends(engine_manager)):
    return await dream('img2img', params, manager)


@router_image.post('/masking')
async def stable_masking(params: TaskParams = Depends(), manager: EngineManager = Depends(engine_manager)):
    return await dream('masking', params, manager)


# TODO 커스텀 모델 기능 개발
@router_image.post('/custom')
async def stable_custom(params: TaskParams = Depends(), manager: EngineManager = Depends(engine_manager)):
    return await dream('txt2img', params, manager)
"""