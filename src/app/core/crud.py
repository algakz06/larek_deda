from time import perf_counter

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.core import models
from app.core import schemas
from app.utils.logging import log
import calendar
from datetime import datetime
import random

# region User
from app.utils.okvd import OKVD


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

    # query(Article).group_by( sa.func.year(Article.created), sa.func.month(Article.created)).all()


def get_company_summary(db: Session, inn: str):

    # create dict with months as keys and count of contracts as values
    cnt_customer = {
        i: {"month": val, "count": 0} for i, val in enumerate(calendar.month_abbr[1:])
    }
    res = (
        db.query(models.Contract)
        .filter(models.Contract.customer_inn == inn)
        .group_by(
            models.Contract.id,
            func.extract("year", models.Contract.sign_date),
            func.extract("month", models.Contract.sign_date),
            # func.month(models.Contract.sign_date),
        )
        .all()
    )
    if not res:
        return []
    kpp = res[0].customer_kpp
    okpd2_code = set()
    for obj in res:
        date = obj.sign_date.month
        cnt_customer[date]["count"] += 1
        okpd2_code.add(obj.okpd2_code)
    print(cnt_customer)

    res = (
        db.query(models.Contract)
        .filter(models.Contract.supplier_inn == inn)
        .group_by(
            models.Contract.id,
            func.extract("year", models.Contract.sign_date),
            func.extract("month", models.Contract.sign_date),
            # func.month(models.Contract.sign_date),
        )
        .all()
    )
    cnt_supplier = {
        i: {"month": val, "count": 0} for i, val in enumerate(calendar.month_abbr[1:])
    }

    for obj in res:
        date = obj.sign_date.month
        cnt_supplier[date]["count"] += 1
        okpd2_code.add(obj.okpd2_code)

    print(cnt_supplier)
    # okved = [
    #     schemas.OKVED(
    #         code=okvd,
    #         type=OKVD[okvd]["type"],
    #         description=OKVD[okvd]["desc"],
    #         date=datetime.fromisoformat(OKVD[okvd]["date"]),
    #     )
    #     for okvd in list(okpd2_code)
    # ]
    print(okpd2_code)
    print(kpp)
    okved = []
    summary = schemas.CompanySummary(
        name="ООО Рога и Копыта",
        inn=int(inn),
        kpp=kpp,
        ogrn=1026605606620,
        registration_date=datetime(year=2010, month=2, day=15),
        creation_date=datetime(year=2010, month=2, day=15),
        registration_authority=6658,
        tax_authority=6671,
        ceo="Иван Иванов Иванович",
        okved=okved,
        contracts_customer=[
            schemas.ContractsAmountByMonth(**i) for i in list(cnt_customer.values())
        ],
        contracts_supplier=[
            schemas.ContractsAmountByMonth(**i) for i in list(cnt_supplier.values())
        ],
        arbitration_cases=[
            schemas.ArbitrationCase(
                **{"month": name[:3], "count": random.randint(0, 5)}
            )
            for name in calendar.month_abbr[1:]
        ],
    )
    return summary


def get_okpd(db: Session) -> list[schemas.OkpdSlim]:
    okpd = db.execute(
        select(models.Okpd)
        .filter(models.Okpd.code.regexp_match("^\\d{2}$"))
        .order_by(models.Okpd.code)
    ).fetchall()

    if not okpd:
        return []

    return [
        schemas.OkpdSlim(
            id=i[0].id,
            section=i[0].section,
            section_name=i[0].section_name,
            code=i[0].code,
            name=i[0].name,
        )
        for i in okpd
    ]


def winrate(db: Session, inn: str):

    res = (
        db.query(models.ParticipationtStat)
        .filter(models.ParticipationtStat.supplier_id == inn)
        .all()
    )
    log.info(res)
    return []


# endregion User
