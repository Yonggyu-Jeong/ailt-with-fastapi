from fastapi import Depends

from app.common.configs.config import DbConfig
from app.database.database import Database
from app.services.user_service import UserService
from tests.user_test.test_user_service import TestUserService

"""
    get_database()
        return Database     

    DbConfig를 이용하여, DataBase를 초기화하고 가져오는 함수입니다.

    작성자 : 정용규
    작성일 : 2024. 01. 16
"""


def get_database() -> Database:
    return Database(DbConfig())


"""
    get_user_service(database: Database)
        return UserService

    Database를 입력 받아, UserService를 초기화하고 가져오는 함수입니다.

    작성자 : 정용규
    작성일 : 2024. 01. 16
"""


def get_user_service(database: Database = Depends(get_database)) -> UserService:
    return UserService(database)


def get_test_user_service(database: Database = Depends(get_database)) -> TestUserService:
    return TestUserService(database)
