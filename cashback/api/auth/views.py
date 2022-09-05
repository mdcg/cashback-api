from cashback import cashback_user_cases
from cashback.api.utils.response import generate_response_payload
from cashback.api.utils.validation.incomming_payload_schemas import (
    authentication_schema,
)
from cashback.domain.exceptions import (
    ResellerNotFoundException,
    UnauthorizedException,
)
from flask import Blueprint, request
from flask_expects_json import expects_json

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/auth", methods=["POST"])
@expects_json(authentication_schema)
def authentication():
    payload = request.json

    email = payload["email"]
    password = payload["password"]

    try:
        auth_token = cashback_user_cases.authenticate_user(
            email=email, password=password
        )
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"email": "Reseller not found."},
            status="fail",
            http_code=404,
        )
    except UnauthorizedException:
        return generate_response_payload(status="fail", http_code=401)

    return generate_response_payload(
        data={"token": auth_token}, status="success", http_code=200
    )
