from time import perf_counter

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core import models
from app.core import schemas
from app.utils.logging import log


# region User


def get_user_by_inn(db: Session, inn: str) -> models.User | None:

    return db.query(models.User).where(models.User.inn == str(inn)).one_or_none()


def create_user(db: Session, data: schemas.UserCreateSchema) -> models.User | None:
    if get_user_by_inn(db, data.inn):
        return None
    db_user = models.User(
        inn=data.inn, hashed_password=data.password, user_type=data.usertype
    )
    db.add(db_user)
    db.commit()
    return db_user


def count_contracts_by_Month(db: Session, inn: str):
    db.query(models.Contract).group_by(func.month(models.Contract.protocol_date)).all()
    
    # query(Article).group_by( sa.func.year(Article.created), sa.func.month(Article.created)).all()


# endregion User
