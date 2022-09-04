from functools import wraps

from cashback import cashback_user_cases
from cashback.api.utils.response import generate_response_payload
from cashback.domain.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
)
from flask import request


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        PREFIX = "Bearer "
        token = None

        if "Authorization" not in request.headers:
            return generate_response_payload(
                data={"message": "Cabeçalho 'Authorization' não informado."},
                status="fail",
                http_code=401,
            )

        token = request.headers["Authorization"]
        if not token.startswith(PREFIX):
            return generate_response_payload(
                data={
                    "message": (
                        "Inclua 'Bearer' no cabeçalho"
                        "'Authorization' informado."
                    )
                },
                status="fail",
                http_code=401,
            )

        try:
            reseller_cpf = (
                cashback_user_cases.extract_reseller_cpf_from_auth_token(
                    token=token[len(PREFIX) :]
                )
            )
        except InvalidTokenException:
            return generate_response_payload(
                data={"message": "Token inválido."},
                status="fail",
                http_code=401,
            )
        except TokenExpiredException:
            return generate_response_payload(
                data={"message": "Token expirado."},
                status="fail",
                http_code=401,
            )

        return f(reseller_cpf, *args, **kwargs)

    return decorator
