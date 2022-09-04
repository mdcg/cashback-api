from cashback.ports.database import DatabasePort

# ToDo:
# 1 - Criar script para provisionar banco de dados (pode inclusive ser um bash) (Done)
# 2 - Criar lógica do PostgreSQLAdapter
# 3 - Criar variáveis de ambiente e testar com o Docker Compose
# 4 - A API externa não está funcionando.. Pensar em um Bypass


class PostgreSQLAdapter(DatabasePort):
    def __init__(self):
        pass

    def create_reseller(self, reseller_payload: dict) -> bool:
        pass

    def get_reseller_by_cpf(self, cpf: str) -> dict:
        pass

    def get_reseller_by_email(self, email: str) -> dict:
        pass

    def create_sale(self, sale_payload: dict) -> bool:
        pass

    def get_sale(self, code: str) -> dict:
        pass

    def get_all_sales_from_a_reseller(self, cpf: str) -> list[dict]:
        pass
