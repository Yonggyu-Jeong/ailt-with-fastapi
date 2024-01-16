from fastapi import FastAPI, Depends
import uvicorn
import app.common.dependencies.dependency as dependency
from app.routers import user_router

"""
    create_app()
        return app

    fast-api를 구동시, config 파일 안의 
    미들웨어 정리, 데이터베이스 초기화, 라우터 정의 및 DB 객체를 다른 라우터에 종속성 주입합니다.

    작성자 : 정용규
    작성일 : 2024. 01. 15
    작성일 : 2024. 01. 14 
"""

app = FastAPI()
database = dependency.get_database()
# TODO 미들웨어 세팅 app.add_middleware()

# TODO 기존 방식으로 TDD 구현시, 기존 dependency 추가 및 추가 코드 필요.
#  router에서 초기화시, 함수의 요청 횟수만큼 초기화되는 일이 발생. 고민 필요.


# TODO depend()는 애플리케이션이 실행되는 동안 한 번 초기화되고 재사용, 그러므로 라우터에서 초기화 가능
#  라우터 전역 의존성에 대해 알아보기. -> app.include에서 의존성 주입 삭제

app.include_router(user_router.router_user, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("shutdown")
def shutdown_db():
    database.close_connection()


# uvicorn 사용하여 FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
