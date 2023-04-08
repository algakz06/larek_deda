from pydantic import BaseModel, Field, EmailStr, validator
from app.core.models import UserType
from datetime import datetime
import calendar
import locale
import random

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

from enum import Enum

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


# region Company


class OKVED(BaseModel):
    type: str = Field(..., max_length=1)
    code: str = Field(...)
    description: str = Field(...)
    date: datetime = Field(...)

    @validator("code", pre=True)
    def check_code(cls, v: str | None):
        if isinstance(v, str):
            if all([c.isdecimal() for c in v.split(".")]):
                return v
            raise ValueError("Invalid OKVED")

    class Config:
        schema_extra = {
            "example": {
                "type": "J",
                "code": "62.01",
                "description": "Разработка компьютерного программного обеспечения",
                "date": datetime(year=2014, month=2, day=1),
            }
        }


def new_cnt() -> int:
    return random.randint(1000, 5000)


class ContractsAmountByMonth(BaseModel):
    month: str = Field(...)
    count: int = Field(default_factory=new_cnt)

    class Config:
        schema_extra = {
            "example": {
                "month": "Январь",
                "count": 1204,
            }
        }


class ArbitrationCase(BaseModel):
    month: str = Field(...)
    count: int = Field(default_factory=new_cnt)

    class Config:
        schema_extra = {
            "example": {
                "month": "Январь",
                "count": 1204,
            }
        }


class CompanySummary(BaseModel):
    name: str = Field(...)
    inn: int = Field(...)
    kpp: int = Field(...)
    ogrn: int = Field(...)
    creation_date: datetime = Field(...)
    registration_authority: int = Field(...)
    tax_authority: int = Field(...)
    registration_date: datetime = Field(...)

    ceo: str = Field(...)
    okved: list[OKVED] = Field(...)
    contracts: list[ContractsAmountByMonth] = Field(...)
    arbitration_cases: list[ArbitrationCase] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Акционерное общество «Производственная Фирма “СКБ Контур”»",
                "inn": 6663003127,
                "kpp": 667101001,
                "ogrn": 1026605606620,
                "creation_date": datetime(year=1992, month=3, day=26),
                "registration_authority": 6658,
                "tax_authority": 6671,
                "registration_date": datetime(year=2020, month=9, day=2),
                "ceo": "Сродных Михаил Юрьевич",
                "okved": [OKVED.Config.schema_extra["example"]],
                "contracts": [
                    {"month": name[:3], "count": random.randint(1000, 5000)}
                    for name in calendar.month_name[1:]
                ],
                "arbitration_cases": [
                    {"month": name[:3], "count": random.randint(0, 5)}
                    for name in calendar.month_name[1:]
                ],
            }
        }


# endregion Company
