from fastapi import Depends

from app.common.configs.config import DbConfig
from app.database.database import Database
from app.services.user_service import UserService

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


