from abc import ABC
from decimal import Decimal


class ExternalRequestPort(ABC):
    def check_accumulated_cashback_from_a_reseller(
        reseller_cpf: str,
    ) -> Decimal:
        pass
