from fastapi import HTTPException, Depends, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from app.image.image_def import get_img_config, get_manager, EngineManager, TaskParams, ImgConfig
from app.image.image_service import dream
import warnings

from tests.image_test import test_txt2img

warnings.filterwarnings(action='ignore')

router_image = APIRouter()

# TODO config와 taskParam은 요청시 마다 가변돼야함.

@router_image.get('/')
def image_home():
    return {"message": "Hello image"}


@router_image.get('/test')
def image_test():
    return test_txt2img()

@router_image.post('/txt2img')
async def stable_txt2img(params: TaskParams, manager: EngineManager = Depends(get_manager)):
    return await dream('txt2img', params, manager)


@router_image.post('/img2img')
async def stable_txt2img(params: TaskParams, manager: EngineManager = Depends(get_manager)):
    return await dream('img2img', params, manager)


@router_image.post('/masking')
async def stable_txt2img(params: TaskParams, manager: EngineManager = Depends(get_manager)):
    return await dream('masking', params, manager)


# TODO 커스텀 모델 기능 개발
@router_image.post('/custom')
async def stable_txt2img(params: TaskParams, manager: EngineManager = Depends(get_manager)):
    return await dream('txt2img', params, manager)


"""
@router_image.get('/custom_models')
async def stable_custom_models(config: ImgConfig = Depends(get_img_config)):
    if config.custom_models is None:
        return JSONResponse(content=[])
    else:
        return JSONResponse(content=config.custom_models)
"""