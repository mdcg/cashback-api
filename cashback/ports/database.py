from abc import ABC, abstractmethod


class DatabasePort(ABC):
    @abstractmethod
    def create_reseller(self, reseller_payload: dict) -> bool:
        pass

    @abstractmethod
    def get_reseller_by_cpf(self, cpf: str) -> dict:
        pass

    @abstractmethod
    def get_reseller_by_email(self, email: str) -> dict:
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
