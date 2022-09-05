import logging
from contextlib import contextmanager
from os import getenv

import psycopg2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[database_script] %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
)
logger.addHandler(handler)

POSTGRESQL_URI = getenv(
    "POSTGRESQL_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


@contextmanager
def get_connection():
    conn = psycopg2.connect(POSTGRESQL_URI)
    cursor = conn.cursor()
    try:
        yield (conn, cursor)
    finally:
        cursor.close()
        conn.close()


def create_cashback_db():
    logger.info("Creating Cashback database...")

    with get_connection() as (conn, cur):
        try:
            cur.execute(
                """
                CREATE TABLE resellers
                    (
                        id serial PRIMARY KEY,
                        fullname varchar,
                        cpf varchar UNIQUE,
                        email varchar UNIQUE,
                        password varchar
                    );
                """
            )
            cur.execute(
                """
                CREATE TABLE sales
                    (
                        id serial PRIMARY KEY,
                        code varchar UNIQUE,
                        date TIMESTAMP,
                        value decimal,
                        reseller_cpf varchar,
                        status varchar
                    );
                """
            )
            conn.commit()

            logger.info("Database created.")
        except psycopg2.DatabaseError as error:
            logger.error(error)


if __name__ == "__main__":
    create_cashback_db()
