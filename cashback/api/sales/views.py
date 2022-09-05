from cashback import cashback_user_cases
from cashback.api.utils.authentication.decorators import token_required
from cashback.api.utils.response import generate_response_payload
from cashback.api.utils.validation.incomming_payload_schemas import sale_schema
from cashback.domain.exceptions import (
    ResellerNotFoundException,
    SaleAlreadyRegistedException,
)
from flask import Blueprint, request
from flask_expects_json import expects_json

sales_blueprint = Blueprint("sales", __name__)


@sales_blueprint.route("/sales", methods=["POST"])
@expects_json(sale_schema)
@token_required
def create_sale(reseller_cpf):
    payload = request.json
    payload["reseller_cpf"] = reseller_cpf

    try:
        cashback_user_cases.create_sale(payload=payload)
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"cpf": "Reseller not found."},
            status="fail",
            http_code=404,
        )
    except SaleAlreadyRegistedException:
        return generate_response_payload(
            data={"code": "Sale already registered."},
            status="fail",
            http_code=400,
        )

    return generate_response_payload(status="success", http_code=201)


@sales_blueprint.route("/sales", methods=["GET"])
@token_required
def list_sales(reseller_cpf):
    try:
        sales = cashback_user_cases.get_reseller_sales(cpf=reseller_cpf)
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"cpf": "Reseller not found."},
            status="fail",
            http_code=404,
        )

    return generate_response_payload(data=sales, status="success")
