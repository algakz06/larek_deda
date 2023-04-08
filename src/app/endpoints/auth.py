from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.schemas import Token
from app.core.auth import authenticate_user, create_access_token, get_password_hash
from app.core.dependencies import get_db
from app.core.settings import settings
from app.utils.logging import log


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # чтобы не редактировать OAuth2PasswordRequestForm предположим, что username = inn
    if not form_data.username.isalnum():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid inn",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = authenticate_user(db, int(form_data.username), form_data.password)
    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect inn or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.inn})  # type: ignore
    token = Token(access_token=access_token, token_type="bearer")
    return token
