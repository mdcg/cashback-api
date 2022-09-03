from cashback.domain.exceptions import (
    ResellerNotFoundException,
    UnauthorizedException,
)
from cashback.domain.models import Reseller, Sale
from cashback.settings import CONFIG


class CashbackAPIUserCases:
    def __init__(self):
        self.database = CONFIG["database"]()
        self.authentication = CONFIG["authentication"]
        self.external_api_communication = CONFIG[
            "external_api_communication"
        ]()

    def authenticate_user(self, email, password):
        reseller_data = self.database.get_reseller_by_email(email)
        if not reseller_data:
            raise ResellerNotFoundException()

        if not self.authentication.check_password(
            reseller_data["password"], password
        ):
            raise UnauthorizedException()

        return self.authentication.encode_auth_token(reseller_data["cpf"])

    def extract_reseller_identifier_from_authentication_token(self, token):
        return self.authentication.decode_auth_token(token)

    def create_reseller(self, payload):
        # Validar payload... Pode ser no próprio Model, chamando por exemplo,
        # um método validate

        # Cria o hash da senha do usuário para ser salva no banco de dados
        payload["password"] = self.authentication.hash_password(
            payload["password"]
        )

        return self.database.create_reseller(payload)

    def get_reseller(self, cpf):
        reseller_data = self.database.get_reseller_by_cpf(cpf)
        if not reseller_data:
            raise ResellerNotFoundException()

        return Reseller(**reseller_data)

    def create_sale(self, payload):
        # Validar payload... Principalmente checando se vem o CPF do reseller
        self.get_reseller(payload.get("reseller_cpf"))
        return self.database.create_sale(payload)

    def get_reseller_sales(self, cpf):
        self.get_reseller(cpf)
        sales = self.database.get_all_sales_from_a_reseller(cpf)
        return [Sale(**sale).to_dict() for sale in sales]
