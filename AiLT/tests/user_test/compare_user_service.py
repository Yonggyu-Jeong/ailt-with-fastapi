from app.models.user_model import UserDto
from app.database.database import Database
from app.services.user_service import UserService

from unittest.mock import Mock, patch
import pytest

# TODO 목업과 pytest를 이용하는 방법으로 개발, 아직 개발 중
class TestUserService:
    def __init__(self, database: Database):
        self.database = database

    def get_user(self):
        user_id = 1
        user_data = {"user_id": user_id, "name": "John Doe"}  # 가상의 유저 데이터

        # Database 클래스의 mock 객체를 생성
        self.database.select_collection.return_value.find_one.return_value = user_data

        # UserService 클래스의 인스턴스를 생성하여 의존성으로 mock된 database를 전달
        user_service = UserService(self.database)

        # 테스트 수행
        result = user_service.get_user(user_id)

        # 호출 여부 검증
        self.database.select_collection.assert_called_once_with("users", user_id)
        self.database.select_collection.return_value.find_one.assert_called_once_with({"user_id": user_id})

        # 결과 검증
        assert result == user_data

        # 반환 값 추가
        return result

    def get_users(self):
        # get_users 메서드를 호출했을 때, database의 __getitem__과 find 메서드가 호출되는지 확인
        user_data_list = [{"user_id": 1, "name": "John Doe"}, {"user_id": 2, "name": "Jane Doe"}]

        # Database 클래스의 mock 객체를 생성
        self.database.__getitem__.return_value.find.return_value = user_data_list

        # UserService 클래스의 인스턴스를 생성하여 의존성으로 mock된 database를 전달
        user_service = UserService(self.database)

        # 테스트 수행
        result = user_service.get_users()

        # 호출 여부 검증
        self.database.__getitem__.assert_called_once_with("users")
        self.database.__getitem__.return_value.find.assert_called_once()

        # 결과 검증
        assert result == user_data_list

        # 반환 값 추가
        return result

    def put_user(self):
        user_id = 1
        user_data = UserDto(id=user_id, age=25, gender=1)

        # Database 클래스의 mock 객체를 생성
        self.database.__getitem__.return_value.update_one.return_value = Mock()

        # UserService 클래스의 인스턴스를 생성하여 의존성으로 mock된 database를 전달
        user_service = UserService(self.database)

        # 테스트 수행
        user_service.put_user(user_id, user_data)

        # 호출 여부 검증
        self.database.__getitem__.assert_called_once_with("users")
        self.database.__getitem__.return_value.update_one.assert_called_once_with({"user_id": user_id},
                                                                                  {"$set": user_data})

    def patch_user(self):
        user_id = 1
        user_data = UserDto(id=user_id, age=30)

        # Database 클래스의 mock 객체를 생성
        self.database.__getitem__.return_value.update_one.return_value = Mock()

        # UserService 클래스의 인스턴스를 생성하여 의존성으로 mock된 database를 전달
        user_service = UserService(self.database)

        # 테스트 수행
        user_service.patch_user(user_id, user_data)

        # 호출 여부 검증
        self.database.__getitem__.assert_called_once_with("users")
        self.database.__getitem__.return_value.update_one.assert_called_once_with({"user_id": user_id},
                                                                                  {"$set": user_data})

    def insert_user(self):
        user_data = UserDto(id=1, age=25, gender=1)

        # Database 클래스의 mock 객체를 생성
        self.database.insert_collection.return_value.insert_one.return_value = Mock()

        # UserService 클래스의 인스턴스를 생성하여 의존성으로 mock된 database를 전달
        user_service = UserService(self.database)

        # 테스트 수행
        user_service.insert_user(user_data)

        # 호출 여부 검증
        self.database.insert_collection.assert_called_once_with("users", user_data)
        self.database.insert_collection.return_value.insert_one.assert_called_once_with(user_data)

    def delete_user(self):
        user_id = 1

        # Database 클래스의 mock 객체를 생성
        self.database.__getitem__.return_value.delete_collection.return_value = Mock()

        # UserService 클래스의 인스턴스를 생성하여 의존성으로 mock된 database를 전달
        user_service = UserService(self.database)

        # 테스트 수행
        user_service.delete_user(user_id)

        # 호출 여부 검증
        self.database.__getitem__.assert_called_once_with("users")
        self.database.__getitem__.return_value.delete_collection.assert_called_once_with({"user_id": user_id})
