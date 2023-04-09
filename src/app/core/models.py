from typing import Optional, Any
from datetime import datetime
from sqlalchemy.types import DateTime, Integer, Date, Boolean, String, BigInteger
from sqlalchemy.dialects.postgresql import MONEY, CHAR, VARCHAR, TEXT, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint
from enum import Enum

from app.core.database import Base


class UserType(Enum):
    supplier = 1
    customer = 2


# region user
class User(Base):
    __tablename__ = "users"
    inn: Mapped[str] = mapped_column("inn", VARCHAR(15), primary_key=True)
    organization_name: Mapped[str] = mapped_column(
        "organization_name", TEXT, nullable=True
    )
    organization_representative: Mapped[str] = mapped_column(
        "organization_representative", TEXT, nullable=True
    )
    hashed_password: Mapped[str] = mapped_column("hashed_password", TEXT, nullable=True)
    user_type = mapped_column("user_type", CHAR(1), nullable=True)
    created_at = mapped_column("created_at", DateTime, default=datetime.utcnow)


class Okpd(Base):
    __tablename__ = "okpd"
    id: Mapped[int] = mapped_column(
        "id", BigInteger, autoincrement=True, primary_key=True
    )
    section: Mapped[str] = mapped_column("section", CHAR(1), nullable=True)
    section_name: Mapped[str] = mapped_column("section_name", TEXT, nullable=True)
    sub_section: Mapped[str] = mapped_column("sub_section", CHAR(2), nullable=True)
    sub_section_name: Mapped[str] = mapped_column(
        "sub_section_name", TEXT, nullable=True
    )
    code: Mapped[str] = mapped_column("code", TEXT, nullable=True)
    name: Mapped[str] = mapped_column("name", TEXT, nullable=True)
    notes: Mapped[str] = mapped_column("notes", TEXT, nullable=True)
    sub_code_1: Mapped[str] = mapped_column("sub_code_1", VARCHAR(4), nullable=True)
    sub_code_2: Mapped[str] = mapped_column("sub_code_2", VARCHAR(4), nullable=True)
    sub_code_3: Mapped[str] = mapped_column("sub_code_3", VARCHAR(4), nullable=True)
    sub_code_4: Mapped[str] = mapped_column("sub_code_4", VARCHAR(4), nullable=True)

    def __repr(self):
        return f"OKPD {self.id} {self.code} {self.name}"


# endregion

# region contract
class EnforcementType(Enum):
    cash_account = 1
    bank_guarantee = 2


class Contract(Base):
    # procedure_id – идентификатор закупки
    __tablename__ = "contracts"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    contract_id = mapped_column("contract_id", VARCHAR(15))
    procedure_id = mapped_column("procedure_id", TEXT)
    customer_inn = mapped_column("customer_inn", VARCHAR(15), nullable=True)
    customer_kpp = mapped_column("customer_kpp", VARCHAR(9), nullable=True)
    protocol_date = mapped_column("protocol_date", Date, nullable=True)
    sign_date = mapped_column("sign_date", Date, nullable=True)
    min_publish_date = mapped_column("min_publish_date", Date, nullable=True)
    contract_subject = mapped_column("contract_subject", TEXT, nullable=True)
    contract_price_rub = mapped_column("contract_price_rub", MONEY, nullable=True)
    advance_sum_percents = mapped_column("advance_sum_percents", MONEY, nullable=True)
    subcontractor_sum_percents = mapped_column(
        "subcontractor_sum_percents", MONEY, nullable=True
    )
    execution_start_date = mapped_column("execution_start_date", Date, nullable=True)
    execution_end_date = mapped_column("execution_end_date", Date, nullable=True)
    enforcement_type = mapped_column("enforcement_type", TEXT, nullable=True)
    enforcement_amount_rub = mapped_column(
        "enforcement_amount_rub", MONEY, nullable=True
    )
    supplier_inn = mapped_column("supplier_inn", VARCHAR(15), nullable=True)
    supplier_kpp = mapped_column("supplier_kpp", VARCHAR(20), nullable=True)
    okpd2_code = mapped_column("okpd2_code", TEXT, nullable=True)


class ContractTermination(Base):
    __tablename__ = "contract_terminations"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    contract_id = mapped_column("contract_id", TEXT, primary_key=True)
    termination_date = mapped_column("termination_date", Date, nullable=True)
    termination_reason_info = mapped_column(
        "termination_reason_info", TEXT, nullable=True
    )
    termination_reason_name = mapped_column(
        "termination_reason_name", TEXT, nullable=True
    )


class ContractImproperExecution(Base):
    __tablename__ = "contract_improper_executions"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    contract_id = mapped_column("contract_id", TEXT, nullable=True)
    execution_info = mapped_column("execution_info", TEXT, nullable=True)
    execution_document_date = mapped_column(
        "execution_document_date", Date, nullable=True
    )
    execution_document_name = mapped_column(
        "execution_document_name", TEXT, nullable=True
    )


# endregion

# region notification
class NotificationInfo(Base):
    __tablename__ = "notification_info"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    procedure_id = mapped_column("procedure_id", TEXT)
    first_publish_day = mapped_column("first_publish_day", Date, nullable=True)
    etp_code = mapped_column("etp_code", TEXT, nullable=True)
    customer_inn = mapped_column("customer_inn", VARCHAR(15), nullable=True)
    customer_kpp = mapped_column("customer_kpp", VARCHAR(9), nullable=True)
    max_price = mapped_column("max_price", MONEY, nullable=True)
    currency_code = mapped_column("currency_code", CHAR(3), nullable=True)
    placing_name = mapped_column("placing_name", TEXT, nullable=True)
    one_side_rejection = mapped_column("one_side_rejection", Boolean, nullable=True)


# endregion

# region complate
class Complaint(Base):
    __tablename__ = "complaints"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    complaint_id = mapped_column("complaint_id", CHAR(6))
    procedure_id = mapped_column("procedure_id", TEXT, nullable=True)
    status = mapped_column("status", TEXT, nullable=True)
    processing_result = mapped_column("processing_result", TEXT, nullable=True)


# endregion

# region participation stat
class ParticipationtStat(Base):
    __tablename__ = "participation_stats"
    __table_args__ = (CheckConstraint("participiant_count >= wins_count"),)
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    supplier_id = mapped_column("supplier_id", VARCHAR(15))
    supplier_kpp = mapped_column("supplier_kpp", VARCHAR(9), nullable=True)
    fz = mapped_column("fz", VARCHAR(5), nullable=True)
    participiant_count = mapped_column("participiant_count", Integer, nullable=True)
    wins_count = mapped_column("wins_count", Integer, nullable=True)


# endregion

# region rnp
class Rnp(Base):
    __tablename__ = "rnp"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    supplier_inn = mapped_column("supplier_inn", VARCHAR(15))
    supplier_kpp = mapped_column("supplier_kpp", VARCHAR(9), nullable=True)
    supplier_reg_number = mapped_column("supplier_reg_number", TEXT, nullable=True)
    include_reason = mapped_column("include_reason", TEXT, nullable=True)
    include_date = mapped_column("include_date", Date, nullable=True)
    exclude_date = mapped_column("exclude_date", Date, nullable=True)


# endregion

# region msp
class OrganizationType(Enum):
    legal_entity = "1"
    individual_entrepreneur = "2"


class OrganizationCategory(Enum):
    micro_enterprise = "1"
    small_enterprise = "2"
    mediumenterprise = "3"


class MspRoster(Base):
    __tablename__ = "msp_roster"
    inn = mapped_column("inn", VARCHAR(15), primary_key=True)
    include_date = mapped_column("include_date", Date, nullable=True)
    organization_type = mapped_column("organization_type", CHAR(1), nullable=True)
    organization_category = mapped_column(
        "organization_category", CHAR(1), nullable=True
    )


# endregion

# region static_codes
class StatisticCodes(Base):
    __tablename__ = "static_codes"
    inn = mapped_column("inn", VARCHAR(15), primary_key=True)
    okato_reg_code = mapped_column("okato_reg_code", TEXT, nullable=True)
    okato_reg_name = mapped_column("okato_reg_name", TEXT, nullable=True)
    okato_fact_code = mapped_column("okato_fact_code", TEXT, nullable=True)
    okato_fact_name = mapped_column("okato_fact_name", TEXT, nullable=True)
    oktmo_reg_code = mapped_column("oktmo_reg_code", TEXT, nullable=True)
    oktmo_reg_name = mapped_column("oktmo_reg_name", TEXT, nullable=True)
    oktmo_fact_code = mapped_column("oktmo_fact_code", TEXT, nullable=True)
    oktmo_fact_name = mapped_column("oktmo_fact_name", TEXT, nullable=True)
    okopf_code = mapped_column("okopf_code", TEXT, nullable=True)
    okopf_name = mapped_column("okopf_name", TEXT, nullable=True)
    okfs_code = mapped_column("okfs_code", TEXT, nullable=True)
    okfs_name = mapped_column("okfs_name", TEXT, nullable=True)
    okogu_code = mapped_column("okogu_code", TEXT, nullable=True)
    okogu_name = mapped_column("okogu_name", TEXT, nullable=True)


# endregion

# region ergul
class EgrulInfo(Base):
    __tablename__ = "egrul_info"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    kpp = mapped_column("kpp", VARCHAR(9), nullable=True)
    registration_date = mapped_column("registration_date", Date, nullable=True)
    entity_state_record_date = mapped_column(
        "entity_state_record_date", Date, nullable=True
    )
    entity_state = mapped_column("entity_state", TEXT, nullable=True)
    termination_date = mapped_column("termination_date", Date, nullable=True)
    termination_way = mapped_column("termination_way", TEXT, nullable=True)
    entity_wo_attorney_type = mapped_column(
        "entity_wo_attorney_type", TEXT, nullable=True
    )
    entity_wo_attorney_position = mapped_column(
        "entity_wo_attorney_position", TEXT, nullable=True
    )
    capital_types = mapped_column("capital_types", TEXT, nullable=True)
    capital_size = mapped_column("capital_size", TEXT, nullable=True)
    okved_basic_code = mapped_column("okved_basic_code", TEXT, nullable=True)
    okved_add_codes = mapped_column("okved_add_codes", ARRAY(String), nullable=True)
    has_filial = mapped_column("has_filial", Boolean, nullable=True)


class EgrulLicences(Base):
    __tablename__ = "egrul_licences"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15), nullable=True)
    license_date = mapped_column("license_date", Date, nullable=True)
    license_start_date = mapped_column("license_start_date", Date, nullable=True)
    license_type = mapped_column("license_type", TEXT, nullable=True)


# endregion

# region egrip
class EgripInfo(Base):
    __tablename__ = "egrip_info"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    is_farm_economy = mapped_column("is_farm_economy", Boolean, nullable=True)
    registration_date = mapped_column("registration_date", Date, nullable=True)
    termination_date = mapped_column("termination_date", Date, nullable=True)
    termination_way = mapped_column("termination_way", TEXT, nullable=True)
    okved_basic_code = mapped_column("okved_basic_code", TEXT, nullable=True)
    okved_add_codes = mapped_column("okved_add_codes", ARRAY(String), nullable=True)


class EgripLicences(Base):
    __tablename__ = "egrip_licences"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15), nullable=True)
    license_date = mapped_column("license_date", Date, nullable=True)
    license_start_date = mapped_column("license_start_date", Date, nullable=True)
    license_end_date = mapped_column("license_end_date", Date, nullable=True)
    license_type = mapped_column("license_type", TEXT, nullable=True)


# endregion

# region staff quantity
class StaffQuantity(Base):
    __tablename__ = "staff_quantity"
    inn = mapped_column("inn", VARCHAR(15), primary_key=True)
    staff_quantity = mapped_column("staff_quantity", Integer, nullable=True)


# endregion

# region balance
class BalanceCodeDict(Base):
    __tablename__ = "balance_code_dict"
    str_code = mapped_column("str_code", TEXT, primary_key=True)
    str_name = mapped_column("str_name", TEXT, nullable=True)


class BalanceSheet(Base):
    __tablename__ = "balance_sheet"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    financial_year = mapped_column("financial_year", Integer)
    str_code = mapped_column("str_code", TEXT, ForeignKey("balance_code_dict.str_code"))
    str_value = mapped_column("str_value", TEXT, nullable=True)


class BalanceCapitalChange1(Base):
    __tablename__ = "balance_capital_change_1"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    financial_year = mapped_column("financial_year", Integer)
    str_code = mapped_column("str_code", TEXT, ForeignKey("balance_code_dict.str_code"))
    auth_capital = mapped_column("auth_capital", TEXT, nullable=True)
    own_shares = mapped_column("own_shares", TEXT, nullable=True)
    extra_capital = mapped_column("extra_capital", TEXT, nullable=True)
    reserve_capital = mapped_column("reserve_capital", TEXT, nullable=True)
    unappropriated_balance = mapped_column(
        "unappropriated_balance", TEXT, nullable=True
    )
    total = mapped_column("total", TEXT, nullable=True)


class BalanceCapitalChange2(Base):
    __tablename__ = "balance_capital_change_2"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    period_description = mapped_column("period_description", TEXT, nullable=True)
    financial_year = mapped_column("financial_year", Integer)
    str_code = mapped_column("str_code", TEXT, ForeignKey("balance_code_dict.str_code"))
    str_value = mapped_column("str_value", TEXT, nullable=True)


class BalanceCapitalChange3(Base):
    __tablename__ = "balance_capital_change_3"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    str_code = mapped_column("str_code", TEXT, ForeignKey("balance_code_dict.str_code"))
    str_value = mapped_column("str_value", TEXT, nullable=True)


class BalanceFinancialResults(Base):
    __tablename__ = "balance_financial_results"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    str_code = mapped_column("str_code", TEXT, ForeignKey("balance_code_dict.str_code"))
    str_value = mapped_column("str_value", TEXT, nullable=True)


class BalanceFundMovement(Base):
    __tablename__ = "balance_fund_movement"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    str_code = mapped_column("str_code", TEXT, ForeignKey("balance_code_dict.str_code"))
    str_value = mapped_column("str_value", TEXT, nullable=True)


class BalanceTargetFundUse(Base):
    __tablename__ = "balance_target_fund_use"
    id = mapped_column("id", BigInteger, autoincrement=True, primary_key=True)
    inn = mapped_column("inn", VARCHAR(15))
    str_code = mapped_column("str_code", TEXT, ForeignKey("balance_code_dict.str_code"))
    str_value = mapped_column("str_value", TEXT, nullable=True)


# endregion
