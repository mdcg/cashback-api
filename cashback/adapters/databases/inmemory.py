from cashback.domain.exceptions import ResellerAlreadyRegistedException
from cashback.ports.database import DatabasePort


class InMemoryAdapter(DatabasePort):
    def __init__(self):
        self.resellers = []
        self.sales = []

    def create_reseller(self, reseller_payload: dict) -> bool:
        if self.get_reseller_by_cpf(cpf=reseller_payload.get("cpf")):
            raise ResellerAlreadyRegistedException()

        self.resellers.append(reseller_payload)
        return True

    def get_reseller_by_cpf(self, cpf: str) -> dict:
        for reseller in self.resellers:
            if reseller.get("cpf") == cpf:
                return reseller
        return None

    def get_reseller_by_email(self, email: str) -> dict:
        for reseller in self.resellers:
            if reseller.get("email") == email:
                return reseller
        return None

    def create_sale(self, sale_payload: dict) -> bool:
        self.sales.append(sale_payload)
        return True

    def get_sale(self, code: str) -> dict:
        for sale in self.sales:
            if sale.get("code") == code:
                return sale
        return None

    def get_all_sales_from_a_reseller(self, cpf: str) -> list[dict]:
        sales_from_reseller = []
        for sale in self.sales:
            if sale.get("reseller_cpf") == cpf:
                sales_from_reseller.append(sale)
        return sales_from_reseller
