from cashback.api.utils.response import generate_response_payload
from cashback.api import cashback_user_cases

from flask import Blueprint, request

sales_blueprint = Blueprint("sales", __name__)


@sales_blueprint.route("/resellers/<string:cpf>/sales", methods=["POST"])
def create_sale(cpf):
    payload = request.json
    payload["reseller_cpf"] = cpf

    cashback_user_cases.create_sale(payload)
    return generate_response_payload(status="success")


@sales_blueprint.route("/resellers/<string:cpf>/sales", methods=["GET"])
def list_sales(cpf):
    return generate_response_payload(
        data=cashback_user_cases.get_reseller_sales(cpf), status="success"
    )
