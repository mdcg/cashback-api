from decimal import Decimal
from enum import Enum

from cashback.settings import AUTOMATIC_APPROVED_RESELLERS_CPFS
from cashback.domain.validators import Validator


class SaleStatus(Enum):
    APPROVED = "Aprovado"
    DENIED = "Recusado"
    WAITING_FOR_VALIDATION = "Em validação"


class Reseller:
    def __init__(
        self,
        fullname: str,
        cpf: str,
        email: str,
        password: str,
        *args: list,
        **kwargs: dict,
    ):
        self.fullname = fullname
        self.cpf = cpf
        self.email = email
        self.password = password

    def validate_register_data(self):
        Validator.validate_fullname(fullname=self.fullname)
        Validator.validate_email(email=self.email)
        Validator.validate_cpf(cpf=self.cpf)
        Validator.validate_password(password=self.password)

    def to_dict(self):
        return {
            "fullname": self.fullname,
            "cpf": self.cpf,
            "email": self.email,
        }


class Sale:
    def __init__(
        self,
        code: str,
        date: str,
        value: Decimal,
        reseller_cpf: str,
        status: str = None,
        *args: list,
        **kwargs: dict,
    ):
        self.code = code
        self.date = date
        self.value = value
        self.reseller_cpf = reseller_cpf
        self.status = status if status else self.process_default_status()

    def process_default_status(self):
        if self.reseller_cpf in AUTOMATIC_APPROVED_RESELLERS_CPFS:
            return SaleStatus.APPROVED.value

        return SaleStatus.WAITING_FOR_VALIDATION.value

    def to_dict(self, include_reseller_cpf=False):
        payload = {
            "code": self.code,
            "date": self.date,
            "value": self.value,
            "status": self.status,
        }

        if include_reseller_cpf:
            payload["reseller_cpf"] = self.reseller_cpf

        return payload


class Cashback:
    def __init__(self, total_sold: list[Sale]):
        self.percentage = self.calculate_percentage(total_sold)

    def calculate_percentage(self, total_sold):
        percentage = None
        if total_sold <= Decimal(1000):
            percentage = Decimal(0.10)
        elif total_sold > Decimal(1000) and total_sold <= Decimal(1500):
            percentage = Decimal(0.15)
        elif total_sold > Decimal(1500):
            percentage = Decimal(0.20)

        return percentage
