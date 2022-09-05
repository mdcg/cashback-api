"""API RESTful Mock

- Não foi possível acessar a API do desafio, por isso, foi criada uma
API bastante simples que consulta no banco de dados as vendas de um
determinado revendedor no último mês e retorna o acumulado do valor total.
"""
from contextlib import contextmanager
from os import getenv

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[MOCK_API] %(asctime)s - %(levelname)s : %(message)s",
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
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        yield (conn, cursor)
    finally:
        cursor.close()
        conn.close()


def accumulated_cashback(cpf):
    with get_connection() as (_, cur):
        cur.execute(
            "SELECT sum(value) as accumulated_cashback FROM sales WHERE reseller_cpf=%s;",
            (cpf,),
        )
        return cur.fetchone()["accumulated_cashback"]


app = Flask(__name__)


@app.route("/v1/cashback", methods=["GET"])
def index():
    args = request.args
    if "cpf" not in args:
        return jsonify({}), 400

    accumulated_cashback_from_cpf = accumulated_cashback(cpf=args["cpf"])
    return (
        jsonify({"accumulated_cashback": accumulated_cashback_from_cpf}),
        200,
    )


app.run(host="0.0.0.0", port="5001", use_reloader=False)
