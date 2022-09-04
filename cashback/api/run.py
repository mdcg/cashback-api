import logging
import signal

from flask import Flask

from cashback.api.auth.views import auth_blueprint
from cashback.api.healthcheck.views import healthcheck_blueprint
from cashback.api.reseller.views import resellers_blueprint
from cashback.api.sales.views import sales_blueprint

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[CASHBACK_API] %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
)
logger.addHandler(handler)


def handle_sigterm(*args):
    """SIGTERM é um sinal conhecido por um processo informático em sistemas
    operativos POSIX. Este é o sinal padrão enviado pelos comandos kill e
    killall. Basicamente ele causa o término do processo, como em SIGKILL,
    porém pode ser interpretado ou ignorado pelo processo. Com isso, SIGTERM
    realiza um encerramento mais amigável, permitindo a liberação de memória e
    o fechamento dos arquivos.
    """
    raise SystemExit


def create_app(*args, **kwargs):
    signal.signal(signalnum=signal.SIGTERM, handler=handle_sigterm)

    app = Flask(__name__)
    app.register_blueprint(blueprint=healthcheck_blueprint)
    app.register_blueprint(blueprint=auth_blueprint)
    app.register_blueprint(blueprint=resellers_blueprint)
    app.register_blueprint(blueprint=sales_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    try:
        app.run(host="0.0.0.0", use_reloader=False) # nosec
    except (KeyboardInterrupt, SystemExit):
        logging.info("Gracefuly stopping Northbound API...")
