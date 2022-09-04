"""Por convenção, as respostas seguiram o padrão JSEND.
Simplificando, JSEND é uma especificação que estabelece algumas regras de
como as respostas JSON de servidores da web devem ser formatadas.
JSEND se concentra em mensagens de nível de aplicativo
(em oposição a nível de protocolo ou transporte), o que o torna ideal
para uso em aplicativos e APIs de estilo REST.

Você pode ler mais sobre esse padrão por aqui:
https://github.com/omniti-labs/jsend
"""
from flask import jsonify

JSEND_RESPONSE_FORMAT = {
    "success": {
        "status": "success",
        "data": None,
    },
    "fail": {
        "status": "fail",
        "data": None,
    },
    "error": {
        "status": "error",
        "message": None,
    },
}


def generate_response_payload(
    data: dict = None,
    status: str = None,
    message: str = None,
    http_code: int = 200,
) -> tuple[dict, int]:
    payload = JSEND_RESPONSE_FORMAT.get(status, "success")

    if "data" in payload:
        payload["data"] = data
    elif "message" in payload:
        payload["message"] = message

    return jsonify(payload), http_code
