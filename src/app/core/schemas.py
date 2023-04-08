from pydantic import BaseModel, Field, EmailStr, validator
from app.core.models import UserType


# region Token
class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "dsjaflkjfkljweqoifjivkdjsa",
                "token_type": "Bearer",
            }
        }


class TokenData(BaseModel):
    inn: str | None = None


# endregion Token


# region User


class UserCreateSchema(BaseModel):
    inn: str = Field(...)
    password: str = Field(...)
    usertype: UserType

    @validator("inn", pre=True)
    def check_inn(cls, v: str):
        if 0 < int(v) < 999999999999:
            return v
        raise ValueError("Invalid inn")

    class Config:
        schema_extra = {
            "example": {
                "inn": 123215677652,
                "password": "SuperStr0ngPassw0rd",
                "usertype": 1,
            }
        }


# endregion User
