from decimal import Decimal
from os import getenv
import requests
from cashback.ports.external_api import ExternalRequestPort
from cashback.domain.exceptions import (
    AccumaltedCashbackAPIUnavailableException,
)

ACCUMULATED_CASHBACK_RESTFUL_API_URL = getenv(
    "ACCUMULATED_CASHBACK_RESTFUL_API_URL",
    "http://localhost:5001/v1/cashback",
)


class RestfulRequestAdapter(ExternalRequestPort):
    @staticmethod
    def check_accumulated_cashback_from_a_reseller(
        reseller_cpf: str,
    ) -> Decimal:
        try:
            response = requests.get(
                f"{ACCUMULATED_CASHBACK_RESTFUL_API_URL}?cpf={reseller_cpf}"
            )
        except requests.exceptions.ConnectionError:
            raise AccumaltedCashbackAPIUnavailableException()

        if response.ok:
            return "{0:.2f}".format(
                Decimal(response.json()["accumulated_cashback"])
            )

        raise AccumaltedCashbackAPIUnavailableException()
