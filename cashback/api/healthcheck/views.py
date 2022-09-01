from cashback.api.utils.response import generate_response_payload

from flask import Blueprint

healthcheck_blueprint = Blueprint("healthcheck", __name__)


@healthcheck_blueprint.route("/")
def ping():
    """Essa é a rota mais simples que é utilizada para verificar
    se a API RESTful está online ou não, literalmente funcionando como
    um ping. Alguns serviços externos podem ser configurados para fazer essa
    verificação automaticamente e detectar indisponibilidades no servidor
    (como New Relic, Dynatrace, Datadog, etc).
    """
    return generate_response_payload(status="success")
