"""Para simular mais um cenário real, nós iremos enfileirar
as compras do revendedor para serem aprovadas (ou não) pelo
nosso worker. Para deixar um pouco dinâmico, uma compra terá
uma chance em dez de ser negada.
"""

import logging
import random
from contextlib import contextmanager
from os import getenv

import pika
import psycopg2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[MOCK_CONSUMER] %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
)
logger.addHandler(handler)

RABBITMQ_HOST = getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = getenv("RABBITMQ_PASS", "guest")

POSTGRESQL_URI = getenv(
    "POSTGRESQL_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


@contextmanager
def get_connection():
    conn = psycopg2.connect(POSTGRESQL_URI)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        yield (conn, cursor)
    finally:
        cursor.close()
        conn.close()


def process_sale(reseller_cpf, sale_code):
    with get_connection() as (_, cur):
        cur.execute(
            "SELECT * FROM sales WHERE reseller_cpf=%s AND code=%s;",
            (reseller_cpf, sale_code),
        )
        sale = cur.fetchone()
        if not sale:
            logger.info(f"Sale {sale_code} not found.")
            return None

        # cur.execute(
        #     "UPDATE sales SET status=%s WHERE reseller_cpf=%s AND code=%s;", (status, reseller_cpf, sale_code),
        # )


def callback(ch, method, properties, body):
    logger.info("Message received...")
    return ch.basic_ack(delivery_tag=method.delivery_tag)


def run():
    logger.info("Consumer started...")
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        RABBITMQ_HOST, RABBITMQ_PORT, "/", credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="sales_queue")
    channel.basic_consume(
        queue="sales_queue", on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


run()
