from fastapi import FastAPI, Depends
import uvicorn
from app.common.configs.config import DbConfig
from app.database.database import Database
from app.routers import user_router
from app.common.logger.logger import logger

"""
    create_app()
        return app

    fast-api를 구동시, config 파일 안의 
    미들웨어 정리, 데이터베이스 초기화, 라우터 정의 및 DB 객체를 다른 라우터에 종속성 주입합니다.

    작성자 : 정용규
    작성일 : 2024. 01. 14 
"""

app = FastAPI()
#TODO 미들웨어 세팅 app.add_middleware()
database = Database(DbConfig())
app.include_router(user_router.router, prefix="/users", tags=["users"], dependencies=[Depends(database)])

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("shutdown")
def shutdown_db():
    database.close_connection()

# uvicorn 사용하여 FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
