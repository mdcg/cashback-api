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
            data={"message": "CPF/E-mail já cadastrado."},
            status="fail",
            http_code=400,
        )
    except InvalidCPFException:
        return generate_response_payload(
            data={"cpf": "CPF inválido."}, status="fail", http_code=400
        )
    except InvalidNameException:
        return generate_response_payload(
            data={"fullname": "Nome inválido."}, status="fail", http_code=400
        )
    except InvalidEmailException:
        return generate_response_payload(
            data={"email": "E-mail inválido."}, status="fail", http_code=400
        )
    except InvalidPasswordException:
        return generate_response_payload(
            data={
                "password": (
                    "Deve ter pelo menos um número, "
                    "pelo menos um caractere maiúsculo e um minúsculo, "
                    "pelo menos um símbolo especial e "
                    "deve ter entre 6 e 20 caracteres."
                )
            },
            status="fail",
            http_code=400,
        )

    return generate_response_payload(status="success", http_code=201)
