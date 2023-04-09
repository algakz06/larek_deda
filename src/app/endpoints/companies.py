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

# create Enum for months


m_index = {index: month for index, month in enumerate(calendar.month_abbr) if month}


router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.get("/{inn}", response_model=schemas.CompanySummary)
async def company_info_by_inn(
    inn: Annotated[int, Path(title="ИНН компании")],
    db: Session = Depends(get_db),
):
    # create dict with months as keys and count of contracts as values
    summary = crud.get_company_summary(db, str(inn))

    return summary
