from cashback.settings import CONFIG
from cashback.domain.models import Reseller, Sale
from cashback.domain.exceptions import ResellerNotFoundException


class CashbackAPIUserCases:
    def __init__(self):
        self.database = CONFIG["database"]
        self.external_api_communication = CONFIG["external_api_communication"]

    def create_reseller(self, payload):
        # Validar payload... Pode ser no próprio Model, chamando por exemplo,
        # um método validate
        return self.database.create_reseller(payload)

    def get_reseller(self, cpf):
        reseller_data = self.database.get_reseller(cpf)
        if not reseller_data:
            raise ResellerNotFoundException()

        return Reseller(**reseller_data)

    def create_sale(self, payload):
        # Validar payload... Principalmente checando se vem o CPF do reseller
        self.get_reseller(payload.get("cpf"))
        return self.database.create_sale(payload)

    def get_reseller_sales(self, cpf):
        self.get_reseller(cpf)
        sales = self.database.get_all_sales_from_a_reseller(cpf)
        return [Sale(**sale) for sale in sales]
