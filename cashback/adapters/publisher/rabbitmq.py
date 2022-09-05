import json
from contextlib import contextmanager
from os import getenv

import pika
from cashback.ports.publisher import MessagePublisherPort

RABBITMQ_HOST = getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = getenv("RABBITMQ_PASS", "guest")
SALES_QUEUE_NAME = getenv("SALES_QUEUE_NAME", "sales_queue")


class RabbitMQPublisher(MessagePublisherPort):
    @contextmanager
    def get_connection(self):
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        parameters = pika.ConnectionParameters(
            RABBITMQ_HOST, RABBITMQ_PORT, "/", credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        try:
            yield (channel, connection)
        finally:
            connection.close()

    def enqueue(self, payload: dict):
        with self.get_connection() as (ch, _):
            ch.basic_publish(
                exchange="",
                routing_key=SALES_QUEUE_NAME,
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                ),
            )
