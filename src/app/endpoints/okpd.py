from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core import schemas
from app.core import crud

from app.core.auth import oauth2_scheme
from app.core.dependencies import get_db

from app.core.settings import settings
from app.utils.logging import log

import calendar
from enum import Enum

router = APIRouter(
    prefix="/okpd",
    tags=["companies"],
)


@router.get("/product/{id}", response_model=list[schemas.Product])
async def product_entrys(
    id: Annotated[int, Path(title="id товара/услуги")],
    db: Session = Depends(get_db),
):
    return [schemas.Product.Config.schema_extra["example"] for i in range(20)]


@router.get("/all", response_model=list[schemas.OkpdSlim])
async def get_product_all(
    db: Session = Depends(get_db),
):
    return crud.get_okpd(db)
