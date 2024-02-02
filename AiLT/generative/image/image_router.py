from fastapi import HTTPException, Depends, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import torch
from PIL import Image
from io import BytesIO
import base64
import diffusers
import json

from generative.image.image_test import EngineManager, dream, TaskParams

router_image = APIRouter()


@router_image.get('/')
def root():
    return {"message": "Hello World"}


@router_image.get('/home')
def home():
    return {"message": "Hello World"}


@router_image.get('/custom_models')
async def stable_custom_models(config: Config = Depends(get_config)):
    if config.custom_models is None:
        return JSONResponse(content=[])
    else:
        return JSONResponse(content=config.custom_models)


@router_image.post('/txt2img')
async def stable_txt2img(params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await dream('txt2img', params, manager)


@router_image.post('/img2img')
async def stable_img2img(params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await dream('img2img', params, manager)


@router_image.post('/masking')
async def stable_masking(params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await dream('masking', params, manager)


# TODO 커스텀 모델 기능 개발
@router_image.post('/custom')
async def stable_custom(params: TaskParams = Depends(), manager: EngineManager = Depends(get_manager)):
    return await dream('txt2img', params, manager)


engine_config = get_config()
engine_manager = get_manager(engine_config)
