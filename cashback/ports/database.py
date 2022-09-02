from abc import ABC, abstractmethod


class DatabasePort(ABC):
    @abstractmethod
    def reseller_authentication(self, email: str, password: str):
        pass

    @abstractmethod
    def create_reseller(self, reseller_payload: dict) -> bool:
        pass

    @abstractmethod
    def get_reseller(self, cpf: str) -> dict:
        pass

    @abstractmethod
    def create_sale(self, sale_payload: dict) -> bool:
        pass

    @abstractmethod
    def get_sale(self, code: str) -> dict:
        pass

    @abstractmethod
    def get_all_sales_from_a_reseller(self, cpf: str) -> list[dict]:
        pass
