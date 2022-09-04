from cashback import cashback_user_cases
from cashback.api.utils.authentication.decorators import token_required
from cashback.api.utils.response import generate_response_payload
from cashback.domain.exceptions import ResellerNotFoundException
from flask import Blueprint, request

sales_blueprint = Blueprint("sales", __name__)


@sales_blueprint.route("/sales", methods=["POST"])
@token_required
def create_sale(cpf):
    payload = request.json
    payload["reseller_cpf"] = cpf

    try:
        cashback_user_cases.create_sale(payload=payload)
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"cpf": "Revendedor não encontrado."},
            status="fail",
            http_code=404,
        )

    return generate_response_payload(status="success", http_code=201)


@sales_blueprint.route("/sales", methods=["GET"])
@token_required
def list_sales(reseller_cpf):
    try:
        sales = cashback_user_cases.get_reseller_sales(cpf=reseller_cpf)
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"cpf": "Revendedor não encontrado."},
            status="fail",
            http_code=404,
        )

    return generate_response_payload(data=sales, status="success")
