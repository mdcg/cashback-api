from cashback.api.utils.response import generate_response_payload
from cashback.api import cashback_user_cases

from flask import Blueprint, request

resellers_blueprint = Blueprint("resellers", __name__)


@resellers_blueprint.route("/resellers", methods=["POST"])
def create_reseller():
    cashback_user_cases.create_reseller(request.json)
    return generate_response_payload(status="success", http_code=201)
