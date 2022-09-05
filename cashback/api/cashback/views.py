from cashback import cashback_user_cases
from cashback.api.utils.response import generate_response_payload
from cashback.api.utils.authentication.decorators import token_required
from cashback.domain.exceptions import (
    ResellerNotFoundException,
    AccumaltedCashbackAPIUnavailableException,
)
from flask import Blueprint

cashback_blueprint = Blueprint("cashback", __name__)


@cashback_blueprint.route("/resellers/cashback", methods=["GET"])
@token_required
def reseller_current_cashback(reseller_cpf):
    try:
        reseller_cashback = (
            cashback_user_cases.get_reseller_accumulated_cashback(
                cpf=reseller_cpf
            )
        )
    except ResellerNotFoundException as error:
        return generate_response_payload(
            data={"cpf": "Revendedor não encontrado."},
            status="fail",
            http_code=404,
        )
    except AccumaltedCashbackAPIUnavailableException as error:
        return generate_response_payload(
            message=(
                "Não foi possível recuperar o cashback acumulado. "
                "Tente novamente mais tarde."
            ),
            status="error",
            http_code=503,
        )

    return generate_response_payload(data={"cashback": reseller_cashback}, status="success")


@cashback_blueprint.route("/sales/cashback", methods=["GET"])
@token_required
def list_sales(reseller_cpf):
    try:
        sales = (
            cashback_user_cases.get_sales_from_reseller_with_cashback_applied(
                cpf=reseller_cpf
            )
        )
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"cpf": "Revendedor não encontrado."},
            status="fail",
            http_code=404,
        )

    return generate_response_payload(data=sales, status="success")
