from contextlib import contextmanager
from os import getenv

import psycopg2
import psycopg2.extras
from cashback.ports.database import DatabasePort
from cashback.domain.exceptions import (
    ResellerAlreadyRegistedException,
    SaleAlreadyRegistedException,
    SaleDatetimeFormatException,
)

POSTGRESQL_URI = getenv(
    "POSTGRESQL_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


class PostgreSQLAdapter(DatabasePort):
    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(POSTGRESQL_URI)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            yield (conn, cursor)
        finally:
            cursor.close()
            conn.close()

    def create_reseller(self, reseller_payload: dict) -> bool:
        with self.get_connection() as (conn, cur):
            try:
                cur.execute(
                    (
                        "INSERT INTO resellers (fullname, cpf, email, password)"
                        "VALUES (%s, %s, %s, %s);"
                    ),
                    (
                        reseller_payload["fullname"],
                        reseller_payload["cpf"],
                        reseller_payload["email"],
                        reseller_payload["password"],
                    ),
                )
                conn.commit()
            except psycopg2.errors.UniqueViolation:
                raise ResellerAlreadyRegistedException()

        return True

    def get_reseller_by_cpf(self, cpf: str) -> dict:
        with self.get_connection() as (_, cur):
            cur.execute("SELECT * FROM resellers WHERE cpf=%s;", (cpf,))
            return cur.fetchone()

    def get_reseller_by_email(self, email: str) -> dict:
        with self.get_connection() as (_, cur):
            cur.execute("SELECT * FROM resellers WHERE email=%s;", (email,))
            return cur.fetchone()

    def create_sale(self, sale_payload: dict) -> bool:
        with self.get_connection() as (conn, cur):
            try:
                cur.execute(
                    (
                        "INSERT INTO sales (code, date, value, reseller_cpf, status)"
                        "VALUES (%s, %s, %s, %s, %s);"
                    ),
                    (
                        sale_payload["code"],
                        sale_payload["date"],
                        sale_payload["value"],
                        sale_payload["reseller_cpf"],
                        sale_payload["status"],
                    ),
                )
                conn.commit()
            except psycopg2.errors.UniqueViolation:
                raise SaleAlreadyRegistedException()
            except psycopg2.errors.DatetimeFieldOverflow:
                raise SaleDatetimeFormatException()

        return True

    def get_sale(self, code: str) -> dict:
        with self.get_connection() as (_, cur):
            cur.execute("SELECT * FROM sales WHERE code=%s;", (code,))
            return cur.fetchone()

    def get_all_sales_from_a_reseller(self, cpf: str) -> list[dict]:
        with self.get_connection() as (conn, cur):
            cur.execute("SELECT * FROM sales WHERE reseller_cpf=%s;", (cpf,))
            return cur.fetchall()

    def get_all_sales_from_a_reseller_from_current_month(
        self, cpf: str
    ) -> list[dict]:
        with self.get_connection() as (conn, cur):
            cur.execute(
                (
                    "SELECT * FROM sales "
                    "WHERE reseller_cpf=%s "
                    "AND extract(YEAR FROM date) = extract(YEAR FROM now()) "
                    "AND extract(MONTH FROM date) = extract(MONTH FROM now());"
                ),
                (cpf,),
            )
            return cur.fetchall()
