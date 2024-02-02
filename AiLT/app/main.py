import uvicorn
from fastapi import FastAPI

import app.common.dependencies.dependency as dependency
from app.routers import user_router
from generative.image import image_service

"""
    fast-api를 구동시 미들웨어 정의, 데이터베이스 초기화, 라우터 정의 합니다.

    작성자 : 정용규
    작성일 : 2024. 01. 15
"""

app = FastAPI()
database = dependency.get_database()
# TODO 미들웨어 세팅 app.add_middleware()

# TODO 기존 방식으로 TDD 구현시, 기존 dependency 추가 및 추가 코드 필요.
#  router에서 초기화 시, 함수의 요청 횟수 만큼 초기화 되는 일이 발생. 고민 필요.


# TODO depend()는 애플리케이션이 실행 되는 동안 한 번 초기화 되고 재사용, 그러므로 라우터에서 초기화 가능
#  라우터 전역 의존성에 대해 알아보기. -> app.include에서 의존성 주입 삭제

app.include_router(user_router.router_user, prefix="/users", tags=["users"])
app.include_router(image_test.router_image, prefix="/images", tags=["images"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("shutdown")
def shutdown_db():
    database.close_connection()


# uvicorn 사용하여 FastAPI 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
