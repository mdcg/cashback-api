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
        reseller_data = self.database.get_reseller_by_email(email=email)
        if not reseller_data:
            raise ResellerNotFoundException()

        if not self.authentication.check_password(
            hashed_password=reseller_data["password"], password=password
        ):
            raise UnauthorizedException()

        return self.authentication.encode_auth_token(
            reseller_cpf=reseller_data["cpf"]
        )

    def extract_reseller_cpf_from_auth_token(self, token):
        return self.authentication.decode_auth_token(auth_token=token)

    def create_reseller(self, payload):
        reseller_data = Reseller(**payload)
        reseller_data.validate_register_data()
        # Cria o hash da senha do usuário para ser salva no banco de dados
        reseller_data.password = self.authentication.hash_password(
            password=reseller_data.password
        )
        return self.database.create_reseller(
            reseller_payload={
                **reseller_data.to_dict(),
                "password": reseller_data.password,
            }
        )

    def get_reseller(self, cpf):
        reseller_data = self.database.get_reseller_by_cpf(cpf=cpf)
        if not reseller_data:
            raise ResellerNotFoundException()

        return Reseller(**reseller_data)

    def create_sale(self, payload):
        # Validar payload... Principalmente checando se vem o CPF do reseller
        self.get_reseller(cpf=payload.get("reseller_cpf"))
        return self.database.create_sale(sale_payload=payload)

    def get_reseller_sales(self, cpf):
        self.get_reseller(cpf)
        sales = self.database.get_all_sales_from_a_reseller(cpf=cpf)
        return [Sale(**sale).to_dict() for sale in sales]
