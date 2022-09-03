from cashback.api import cashback_user_cases
from cashback.api.utils.response import generate_response_payload
from cashback.domain.exceptions import ResellerNotFoundException
from flask import Blueprint, request

sales_blueprint = Blueprint("sales", __name__)


@sales_blueprint.route("/resellers/<string:cpf>/sales", methods=["POST"])
def create_sale(cpf):
    payload = request.json
    payload["reseller_cpf"] = cpf

    try:
        cashback_user_cases.create_sale(payload)
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"cpf": "Reseller not found."}, status="fail", http_code=404
        )

    return generate_response_payload(status="success", http_code=201)


@sales_blueprint.route("/resellers/<string:cpf>/sales", methods=["GET"])
def list_sales(cpf):
    try:
        sales = cashback_user_cases.get_reseller_sales(cpf)
    except ResellerNotFoundException:
        return generate_response_payload(
            data={"cpf": "Reseller not found."}, status="fail", http_code=404
        )

    return generate_response_payload(data=sales, status="success")
