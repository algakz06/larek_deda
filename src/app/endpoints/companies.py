from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.schemas import Token, UserCreateSchema
from app.core.crud import create_user

from app.core.auth import oauth2_scheme
from app.core.dependencies import get_db

from app.core.settings import settings
from app.utils.logging import log


router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.get("/{inn}")
async def company_info_by_inn(
    inn: Annotated[int, Path(title="ИНН компании")],
    db: Session = Depends(get_db),
):
    return {
        "name": "Акционерное общество «Производственная Фирма “СКБ Контур”»",
        "inn": 6663003127,
        "kpp": 667101001,
        "ogrn": 1026605606620,
        "creation_date": datetime(year=1992, month=3, day=26),
        "registration_authority": 6658,
        "tax_authority": 6671,
        "registration_date": datetime(year=2020, month=9, day=2),
        "ceo": "Сродных Михаил Юрьевич",
        "okved": [
            {
                "type": "J",
                "code": "62.01",
                "description": "Разработка компьютерного программного обеспечения",
                "date": datetime(year=2014, month=2, day=1),
            }
        ],
    }
