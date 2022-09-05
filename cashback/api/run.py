import signal

from flask import Flask
from jsonschema import ValidationError

from cashback.api.auth.views import auth_blueprint
from cashback.api.cashback.views import cashback_blueprint
from cashback.api.healthcheck.views import healthcheck_blueprint
from cashback.api.reseller.views import resellers_blueprint
from cashback.api.sales.views import sales_blueprint
from cashback.api.utils.logging import logger
from cashback.api.utils.response import generate_response_payload


def handle_sigterm(*args):
    """SIGTERM é um sinal conhecido por um processo informático em sistemas
    operativos POSIX. Este é o sinal padrão enviado pelos comandos kill e
    killall. Basicamente ele causa o término do processo, como em SIGKILL,
    porém pode ser interpretado ou ignorado pelo processo. Com isso, SIGTERM
    realiza um encerramento mais amigável, permitindo a liberação de memória e
    o fechamento dos arquivos.
    """
    raise SystemExit


def bad_request_handler(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return generate_response_payload(
            data={"error": original_error.message},
            status="fail",
            http_code=400,
        )

    return error


def create_app(*args, **kwargs):
    signal.signal(signalnum=signal.SIGTERM, handler=handle_sigterm)

    app = Flask(__name__)

    app.register_error_handler(400, bad_request_handler)

    app.register_blueprint(blueprint=healthcheck_blueprint)
    app.register_blueprint(blueprint=auth_blueprint)
    app.register_blueprint(blueprint=resellers_blueprint)
    app.register_blueprint(blueprint=sales_blueprint)
    app.register_blueprint(blueprint=cashback_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    try:
        logger.info("Starting Cashback API...")
        app.run(host="0.0.0.0", use_reloader=False)  # nosec
    except (KeyboardInterrupt, SystemExit):
        logger.info("Gracefuly stopping Cashback API...")
