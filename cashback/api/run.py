import logging
import signal

from cashback.api.healthcheck.views import healthcheck_blueprint

from flask import Flask

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


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)

    app = Flask(__name__)
    app.register_blueprint(healthcheck_blueprint, url_prefix="/healthcheck")

    try:
        app.run(host="0.0.0.0", use_reloader=False)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Gracefuly stopping Northbound API...")