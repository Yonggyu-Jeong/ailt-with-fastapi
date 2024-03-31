from app.models.model import ModelDto

"""
    class UserDto(ModelDto)
        
    부모 클래스인 model의 ModelDto를 상속받은 모델입니다.     

    작성자 : 정용규
    작성일 : 2024. 01. 16   
"""


class UserDto(ModelDto):
    id: int
    age: int
    gender: int
