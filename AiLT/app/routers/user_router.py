from fastapi import APIRouter, Depends, HTTPException
from app.models.user_model import UserDto
#from app.common.dependencies.dependency import get_test_user_service as get_user_service
#from tests.user_test.test_user_service import TestUserService as UserService
from app.common.dependencies.dependency import get_user_service
from app.services.user_service import UserService

router_user = APIRouter()


@router_user.get("/")
def read_users(user_service: UserService = Depends(get_user_service)):
    try:
        users = user_service.get_users()
        return users

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router_user.get("/{user_id}")
def read_user(user_id: int,
              user_service: UserService = Depends(get_user_service)):
    try:
        user = user_service.get_user(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router_user.post("/users/")
def create_user(user_data: UserDto,
                user_service: UserService = Depends(get_user_service)):
    try:
        user_service.create_user(user_data)
        return {"message": "create_user successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router_user.put("/{user_id}")
def update_user(user_id: int, user_data: UserDto,
                user_service: UserService = Depends(get_user_service)):
    try:
        user_service.put_user(user_id, user_data)
        return {"message": f"put_user successfully: {user_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router_user.patch("/{user_id}")
def update_user(user_id: int, user_data: UserDto,
                user_service: UserService = Depends(get_user_service)):
    try:
        user_service.patch_user(user_id, user_data)
        return {"message": f"patch_user successfully: {user_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router_user.delete("/{user_id}")
def delete_user(user_id: int,
                user_service: UserService = Depends(get_user_service)):
    try:
        user_service.delete_user(user_id)
        return {"message": f"delete_user successfully: {user_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
