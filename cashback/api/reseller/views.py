from cashback import cashback_user_cases
from cashback.api.utils.response import generate_response_payload
from cashback.api.utils.validation.incomming_payload_schemas import (
    reseller_schema,
)
from cashback.domain.exceptions import (
    InvalidCPFException,
    InvalidEmailException,
    InvalidNameException,
    InvalidPasswordException,
    ResellerAlreadyRegistedException,
)
from flask import Blueprint, request
from flask_expects_json import expects_json

resellers_blueprint = Blueprint("resellers", __name__)


@resellers_blueprint.route("/resellers", methods=["POST"])
@expects_json(reseller_schema)
def create_reseller():
    try:
        cashback_user_cases.create_reseller(payload=request.json)
    except ResellerAlreadyRegistedException:
        return generate_response_payload(
            data={"message": "CPF/E-mail already registered."},
            status="fail",
            http_code=400,
        )
    except InvalidCPFException:
        return generate_response_payload(
            data={"cpf": "Invalid CPF."}, status="fail", http_code=400
        )
    except InvalidNameException:
        return generate_response_payload(
            data={"fullname": "Invalid name."}, status="fail", http_code=400
        )
    except InvalidEmailException:
        return generate_response_payload(
            data={"email": "Invalid e-mail."}, status="fail", http_code=400
        )
    except InvalidPasswordException:
        return generate_response_payload(
            data={
                "password": (
                    "It must have at least one number, at least one uppercase "
                    "and one lowercase character, at least one special symbol, "
                    "and must be between 6 and 20 characters long."
                )
            },
            status="fail",
            http_code=400,
        )

    return generate_response_payload(status="success", http_code=201)
