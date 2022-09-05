from decimal import Decimal

from cashback.domain.exceptions import (
    ResellerNotFoundException,
    UnauthorizedException,
)
from cashback.domain.models import Cashback, Reseller, Sale
from cashback.settings import CONFIG


class CashbackAPIUserCases:
    def __init__(self):
        self.database = CONFIG["database"]()
        self.publisher = CONFIG["publisher"]()
        self.authentication = CONFIG["authentication"]
        self.accumulated_cashback_api = CONFIG["accumulated_cashback_api"]

    def authenticate_user(self, email: str, password: str) -> str:
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

    def extract_reseller_cpf_from_auth_token(self, token: str) -> str:
        return self.authentication.decode_auth_token(auth_token=token)

    def create_reseller(self, payload: dict) -> bool:
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

    def get_reseller(self, cpf: str) -> Reseller:
        reseller_data = self.database.get_reseller_by_cpf(cpf=cpf)
        if not reseller_data:
            raise ResellerNotFoundException()

        return Reseller(**reseller_data)

    def create_sale(self, payload: dict) -> bool:
        self.get_reseller(cpf=payload.get("reseller_cpf"))
        sale_payload = Sale(**payload).to_dict(include_reseller_cpf=True)
        # Publica as informações da venda para serem processadas
        # pelo Worker (Mock Consumer).
        self.publisher.enqueue(payload=sale_payload)
        return self.database.create_sale(sale_payload=sale_payload)

    def get_reseller_sales(self, cpf: str) -> list[dict]:
        self.get_reseller(cpf)
        sales = self.database.get_all_sales_from_a_reseller(cpf=cpf)
        return [Sale(**sale).to_dict() for sale in sales]

    def get_sales_from_reseller_with_cashback_applied(
        self, cpf: str
    ) -> list[dict]:
        self.get_reseller(cpf)
        sales = self.database.get_all_sales_from_a_reseller_from_current_month(
            cpf=cpf
        )
        parsed_sales = [Sale(**sale) for sale in sales]
        cashback = Cashback(parsed_sales)
        return {
            "cashback_percentage": "{0:.2f}".format(cashback.percentage),
            "sales": cashback.calculate_cashback_value_to_sales(),
        }

    def get_reseller_accumulated_cashback(self, cpf: str) -> Decimal:
        return self.accumulated_cashback_api.check_accumulated_cashback_from_a_reseller(  # noqa
            reseller_cpf=cpf
        )
