from pydantic import BaseModel

class UserDto(BaseModel):
    user: str