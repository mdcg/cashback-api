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
    data=None, status=None, message=None, http_code=200
):
    """Formata a mensagem de resposta da requisição seguindo o padrão JSEND.
    Parameters
    ----------
    data : dict, optional
        Todo resultado gerado pela API que seja pertinente ao usuário final
        deve ser descrito aqui. Esse parâmetro é opcional, então caso você
        não queira transmitir nada para o usuário, a resposta será None.
    status : str, optional
        O formato JSEND possui três tipos de status: success, fail e error.
        Cada um desses formatos possuem especificidades em seu payload, por
        isso, geramos o mesmo com base nesse parâmetro.
    http_code : int, optional
        Código de status HTTP seguindo os padrões estabelecidos pela IETF
        (RFC 7231). Caso nenhum parâmetro relacionado seja informado,
        assumiremos que o status HTTP será 200.
    message : str, optional
        Esse parâmtro é específico para o status "error" do JSEND. Caso haja
        algum problema do lado do servidor (500) nós informaremos ao usuário a
        partir desse parâmetro.
    Returns
    -------
    tuple
        Tupla contendo a resposta da requisição no formato JSON e o status
        HTTP.
    """
    payload = JSEND_RESPONSE_FORMAT.get(status, "success")

    if "data" in payload:
        payload["data"] = data
    elif "message" in payload:
        payload["message"] = message

    return jsonify(payload), http_code
