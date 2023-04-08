from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.core.schemas import Token, UserCreateSchema
from app.core.crud import create_user

from app.core.auth import authenticate_user, create_access_token, get_password_hash
from app.core.dependencies import get_db

from app.core.settings import settings
from app.utils.logging import log


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create")
async def create_new_user(
    user_data: UserCreateSchema,
    db: Session = Depends(get_db),
):
    user_data.password = get_password_hash(user_data.password)
    user = create_user(db, user_data)
    if not user:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
        )
    access_token = create_access_token(data={"sub": user.inn})  # type: ignore
    token = Token(access_token=access_token, token_type="bearer")
    return token
