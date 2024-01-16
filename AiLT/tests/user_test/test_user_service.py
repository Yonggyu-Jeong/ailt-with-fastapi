from app.models.user_model import UserDto
from app.database.database import Database
from app.common.logger.logger import logger


class TestUserService:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user_data: UserDto):
        return self.database.insert_collection("users", user_data)

    def get_user(self, user_id: int):
        return self.database.select_collection("users", {"user_id": user_id})

    def get_users(self):
        return self.database.select_collections("users", {})

    def update_user(self, user_id: int, user_data: UserDto):
        return self.database.update_collection("users", {"user_id": user_id}, user_data)

    def delete_user(self, user_id: int):
        return self.database.delete_collection("users", {"user_id": user_id})
