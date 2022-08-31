from abc import ABC, abstractmethod
from cashback.domain.models import Reseller, Sale


class DatabasePort(ABC):
    @abstractmethod
    def reseller_authentication(self, email: str, password: str):
        pass

    @abstractmethod
    def create_reseller(self, reseller_payload: Reseller) -> bool:
        pass

    @abstractmethod
    def get_reseller(self, cpf: str) -> Reseller:
        pass

    @abstractmethod
    def create_sale(self, sale_payload: Sale) -> bool:
        pass

    @abstractmethod
    def get_sale(self, code: str) -> Sale:
        pass

    @abstractmethod
    def get_all_sales_from_a_reseller(self, cpf: str) -> list[Sale]:
        pass
