from cashback.ports.database import DatabasePort


class InMemoryAdapter(DatabasePort):
    def __init__(self):
        self.resellers = []
        self.sales = []

    def reseller_authentication(self, email: str, password: str):
        pass

    def create_reseller(self, reseller_payload: dict) -> bool:
        self.resellers.append(reseller_payload)
        return True

    def get_reseller(self, cpf: str) -> dict:
        for reseller in self.resellers:
            if reseller.get("cpf") == cpf:
                return reseller
        return None

    def create_sale(self, sale_payload: dict) -> bool:
        self.sale.append(sale_payload)
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
