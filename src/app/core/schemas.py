from pydantic import BaseModel, Field, EmailStr
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
    inn: int = Field(..., ge=1)
    password: str = Field(...)
    usertype: UserType

    class Config:
        schema_extra = {
            "example": {
                "inn": "1232156776521",
                "password": "SuperStr0ngPassw0rd",
                "usertype": 1,
            }
        }


# endregion User
