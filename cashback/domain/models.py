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
            "value": "{0:.2f}".format(Decimal(self.value)),
            "status": self.status,
        }

        if include_reseller_cpf:
            payload["reseller_cpf"] = self.reseller_cpf

        return payload


class Cashback:
    def __init__(self, sales_in_current_month: list[Sale]):
        self.__sales = sales_in_current_month
        self.__total_sold = self.total_sales_value()
        self.percentage = self.calculate_percentage()

    def total_sales_value(self):
        total = Decimal(0)
        for sale in self.__sales:
            if sale.status == SaleStatus.APPROVED.value:
                total += Decimal(sale.value)

        return total

    def calculate_percentage(self):
        percentage = None
        if self.__total_sold <= Decimal(1000):
            percentage = Decimal(0.10)
        elif self.__total_sold > Decimal(
            1000
        ) and self.__total_sold <= Decimal(1500):
            percentage = Decimal(0.15)
        elif self.__total_sold > Decimal(1500):
            percentage = Decimal(0.20)
        return percentage

    def calculate_cashback_value_to_sales(self):
        sales_with_cashback_value = []
        for sale in self.__sales:
            cashback = 0
            if sale.status == SaleStatus.APPROVED.value:
                cashback = "{0:.2f}".format(self.percentage * Decimal(sale.value))

            sales_with_cashback_value.append(
                {**sale.to_dict(), "cashback": cashback}
            )

        return sales_with_cashback_value
