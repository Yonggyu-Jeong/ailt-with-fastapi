from app.models.user_model import UserDto
from app.database.database import Database
from app.common.logger.logger import logger


# TODO 로그 기록 방법 통일화. 로거에서 디폴트 메세지 정의 ->
#  별도로 성공 여부 포맷까지 지정시 사용 번거로움 보류.
class UserService:
    def __init__(self, database: Database):
        self.database = database

    # users 컬렉션에 사용자 생성
    def create_user(self, user_data: UserDto):
        try:
            user_collection = self.database.insert_collection("users", user_data)
            user_collection.insert_one(user_data)
            logger.info(f"create_user successfully: {user_data}")

        except Exception as e:
            logger.error(f"Error create_user: {e}")

    # users 컬렉션에서 user_id에 해당하는 사용자 조회
    def get_user(self, user_id: int):
        try:
            user_collection = self.database.select_collection("users", user_id)
            user = user_collection.find_one({"user_id": user_id})
            logger.info(f"get_user successfully: {user}")
            return user

        except Exception as e:
            logger.error(f"Error get_user: {e}")
            return None

    # users 컬렉션에서 모든 사용자 조회
    def get_users(self):
        try:
            user_collection = self.database["users"]
            users = user_collection.find()
            user_list = list(users)
            logger.info(f"get_users successfully: {user_list}")
            return user_list

        except Exception as e:
            logger.error(f"Error get_users: {e}")
            return []

    # users 컬렉션에서 user_id에 해당하는 사용자 업데이트
    def update_user(self, user_id: int, user_data: UserDto):
        try:
            user_collection = self.database["users"]
            user_collection.update_one({"user_id": user_id}, {"$set": user_data})
            logger.info(f"update_user successfully: {user_id}")

        except Exception as e:
            logger.error(f"Error update_user: {e}")

    # users 컬렉션에서 user_id에 해당하는 사용자 부분적으로 업데이트 (PATCH)
    def patch_user(self, user_id: int, user_data: UserDto):
        try:
            user_collection = self.database["users"]
            user_collection.update_one({"user_id": user_id}, {"$set": user_data})
            logger.info(f"patch_user successfully: {user_id}")

        except Exception as e:
            logger.error(f"Error patch_user: {e}")

    # users 컬렉션에서 user_id에 해당하는 사용자 전체 업데이트 (PUT)
    def put_user(self, user_id: int, user_data: UserDto):
        try:
            user_collection = self.database["users"]
            user_collection.update_one({"user_id": user_id}, {"$set": user_data})
            logger.info(f"put_user successfully: {user_id}")

        except Exception as e:
            logger.error(f"Error put_user: {e}")

    # users 컬렉션에서 user_id에 해당하는 사용자 삭제
    def delete_user(self, user_id: int):
        try:
            user_collection = self.database["users"]
            user_collection.delete_collection({"user_id": user_id})
            logger.info(f"delete_user successfully: {user_id}")

        except Exception as e:
            logger.error(f"Error delete_user: {e}")
