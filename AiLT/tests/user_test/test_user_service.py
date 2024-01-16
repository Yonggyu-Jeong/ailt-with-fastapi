from app.database.database import Database

# TODO 가비지 데이터를 제공하는 스텁, user_service와 값을 비교한 함수 별도 개발 예정.
class TestUserService:
    def __init__(self, database: Database):
        self.database = database

    def get_user(self):
        garbage_data = {"user_id": 1, "name": "John Doe"}

        return garbage_data

    def get_users(self):
        garbage_data_list = [{"user_id": 1, "name": "John Doe"}, {"user_id": 2, "name": "Jane Doe"}]

        return garbage_data_list

    def put_user(self):
        garbage_data = {"acknowledged": True, "matched_count": 1, "modified_count": 1}

        return garbage_data

    def patch_user(self):
        garbage_data = {"acknowledged": True, "matched_count": 1, "modified_count": 1}
        return garbage_data

    def insert_user(self):
        garbage_data = {"acknowledged": True, "inserted_id": 'ObjectId'("60d6f8c00a360a4d477f869a")}
        return garbage_data

    def delete_user(self):
        garbage_data = {"acknowledged": True, "deleted_count": 1}
        return garbage_data
