from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core import schemas
from app.core.crud import create_user

from app.core.auth import oauth2_scheme
from app.core.dependencies import get_db

from app.core.settings import settings
from app.utils.logging import log


router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.get("/{inn}", response_model=schemas.CompanySummary)
async def company_info_by_inn(
    inn: Annotated[int, Path(title="ИНН компании")],
    db: Session = Depends(get_db),
):
    return schemas.CompanySummary.Config.schema_extra["example"]


@router.get("/product/{id}", response_model=list[schemas.Product])
async def product_entrys(
    id: Annotated[int, Path(title="id товара/услуги")],
    db: Session = Depends(get_db),
):
    return [schemas.Product.Config.schema_extra["example"] for i in range(20)]
