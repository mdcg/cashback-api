from decimal import Decimal
from enum import Enum
from cashback.settings import AUTOMATIC_APPROVED_RESELLERS_CPFS


class SaleStatus(Enum):
    APPROVED = "Aprovado"
    DENIED = "Recusado"
    WAITING_FOR_VALIDATION = "Em validação"


class Sale:
    def __init__(
        self,
        code: str,
        date: str,
        value: Decimal,
        status: SaleStatus,
        reseller_cpf: str,
    ):
        self.code = code
        self.date = date
        self.value = value
        self.status = self.process_default_status()
        self.reseller_cpf = reseller_cpf

    def process_default_status(self):
        if self.reseller_cpf in AUTOMATIC_APPROVED_RESELLERS_CPFS:
            return SaleStatus.APPROVED

        return SaleStatus.WAITING_FOR_VALIDATION


class Reseller:
    def __init__(self, fullname: str, cpf: str, email: str, password: str):
        self.fullname = fullname
        self.cpf = cpf
        self.email = email
        self.__password = password


class Cashback:
    def __init__(self, sales_in_current_month: list[Sale]):
        self.__sales = sales_in_current_month
        self.__total_sold = self.total_sales_value()
        self.percentage = self.apply_cashbask_percentage()

    def calculate_cashback(self):
        pass

    def total_sales_value(self):
        pass

    def apply_cashbask_percentage(self):
        pass
