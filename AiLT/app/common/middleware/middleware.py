import time
from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
app = FastAPI()

# 참조 문서 https://fastapi.tiangolo.com/advanced/middleware/

#TODO 작성 중 토큰, 쿠키 기능 예정
#TODO DB 작업 이후 할 예정
"""
    prev_process_recodring(request: Request, call_next)
        return response
    
    리퀘스트를 수행하기 전 요청자의 요청 기록 및 헤더를 
    DB에 저장하기 위한 미들웨어입니다. 
    작성자 : 정용규
    작성일 : 2024. 01. 14     
"""
@app.middleware("http")
async def prev_process_recodring(request: Request):
    client_host = request.client.host


#TODO IP호스팅 후 추가할 미들 웨어
"""
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["ailt.com", "*.ailt.com"]
)
"""