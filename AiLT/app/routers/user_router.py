from fastapi import APIRouter, Depends, HTTPException
from app.models.user_model import UserDto
from app.common.logger.logger import logger
from app.common.dependencies.dependency import get_test_user_service as get_user_service
from tests.user_test.test_user_service import TestUserService as UserService

# from app.common.dependencies.dependency import get_user_service
# from app.services.user_service import UserService

router_user = APIRouter()


# TODO depend()를 이용한 라우터 전역 의존성 함수 테스팅. TDD 방식으로 코드 테스트
# TODO TDD 방법론 다시 공부, 주석 처리 방법

@router_user.get("/")
def read_users(user_service: UserService = Depends(get_user_service)):
    users = user_service.get_users()
    return users


@router_user.get("/{user_id}")
def read_user(user_id: int,
              user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router_user.post("/users/")
def create_user(user_data: UserDto,
                user_service: UserService = Depends(get_user_service)):
    user_service.create_user(user_data)
    return {"message": "User created successfully"}


@router_user.patch("/{user_id}")
def update_user(user_id: int,
                user_data: UserDto,
                user_service: UserService = Depends(get_user_service)):
    user_service.update_user(user_id, user_data)
    return {"message": f"User with ID {user_id} updated successfully"}


def put_user(user_id: int,
             user_data: UserDto,
             user_service: UserService = Depends(get_user_service)
):
    user_service.update_user(user_id, user_data)
    return {"message": f"User with ID {user_id} updated successfully"}


@router_user.delete("/{user_id}")
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user_service.delete_user(user_id)
    return {"message": f"User with ID {user_id} deleted successfully"}
