from fastapi import FastAPI
import uvicorn

import app.common.middleware as middleware
from app.common.configs.config import DbConfig, LoggingConfig
from app.database.database import Database
import logging

database = 0


"""
    create_app()
        return app

    fast-api를 구동시, config 파일 안의 
    데이터베이스 초기화, 미들웨어 정리, 라우터 정의를 차례대로 시작합니다. 

    작성자 : 정용규
    작성일 : 2024. 01. 14 
"""
def create_app():
        app = FastAPI()
        db_config = DbConfig()
        database = Database(db_config)
        LoggingConfig()
        #app.add_middleware(middleware)

        return app


app = create_app()


@app.get("/")
async def root():

    return {"message": "Hello World"}





# uvicorn 사용하여 FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# app.include_router()
