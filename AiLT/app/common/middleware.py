import time
from fastapi import FastAPI, Request

app = FastAPI()

"""
TODO 작성 중 
    토큰, 쿠키 기능 예정 
prev_process_recodring(request: Request, call_next)
    return response
    
    리퀘스트를 수행하기 전 요청자의 헤더를 
    DB에 저장하기 위한 미들웨어입니다. 
    작성자 : 정용규
    작성일 : 2024. 01. 14     
"""

@app.middleware("http")
async def prev_process_recodring(request: Request):
    client_host = request.client.host

    #

    return response