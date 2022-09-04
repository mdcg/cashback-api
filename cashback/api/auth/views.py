from cashback import cashback_user_cases
from cashback.api.utils.response import generate_response_payload
from cashback.domain.exceptions import (
    ResellerNotFoundException,
    UnauthorizedException,
)
from flask import Blueprint, request

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/auth", methods=["POST"])
def authentication():
    payload = request.json
    try:
        email = payload["email"]
        password = payload["password"]
    except KeyError:
        return generate_response_payload(
            data={
                "email": "Este campo é obrigatório.",
                "password": "Este campo é obrigatório.",
            },
            status="fail",
            http_code=400,
        )

    try:
        auth_token = cashback_user_cases.authenticate_user(
            email=email, password=password
        )
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"email": "Revendedor não encontrado."},
            status="fail",
            http_code=404,
        )
    except UnauthorizedException:
        return generate_response_payload(status="fail", http_code=401)

    return generate_response_payload(
        data={"token": auth_token}, status="success", http_code=200
    )
