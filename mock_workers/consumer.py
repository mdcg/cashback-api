"""Para simular mais um cenário real, nós iremos enfileirar
as compras do revendedor para serem aprovadas (ou não) pelo
nosso worker. Para deixar um pouco dinâmico, uma compra terá
uma chance em dez de ser negada.
"""

import json
import logging
import random
import time
from contextlib import contextmanager
from os import getenv

import pika
import psycopg2
import psycopg2.extras

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
SALES_QUEUE_NAME = getenv("SALES_QUEUE_NAME", "sales_queue")

POSTGRESQL_URI = getenv(
    "POSTGRESQL_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


def random_status():
    number = random.randint(0, 10)
    return "Negado" if number == 3 else "Aprovado"


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
    with get_connection() as (conn, cur):
        # Aguarda um tempinho, para simular um processamento.
        time.sleep(5)

        cur.execute(
            "SELECT * FROM sales WHERE reseller_cpf=%s AND code=%s;",
            (reseller_cpf, sale_code),
        )
        sale = cur.fetchone()
        if not sale:
            logger.info(f"Sale {sale_code} not found.")
            return None

        status = random_status()

        logger.info(
            f"Venda {sale_code} - Revendedor {reseller_cpf} - Status {status}"
        )

        cur.execute(
            "UPDATE sales SET status=%s WHERE reseller_cpf=%s AND code=%s;",
            (random_status(), reseller_cpf, sale_code),
        )
        conn.commit()


def callback(ch, method, properties, body):
    logger.info("Message received...")
    body = json.loads(body)
    process_sale(reseller_cpf=body["reseller_cpf"], sale_code=body["code"])
    return ch.basic_ack(delivery_tag=method.delivery_tag)


def run():
    logger.info("Consumer started...")
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        RABBITMQ_HOST, RABBITMQ_PORT, "/", credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=SALES_QUEUE_NAME)
    channel.basic_consume(
        queue=SALES_QUEUE_NAME,
        on_message_callback=callback,
    )
    channel.start_consuming()


run()
