from cashback.domain.user_cases import CashbackAPIUserCases
from cashback.settings import CONFIG

database = CONFIG["database"]()
publisher = CONFIG["publisher"]()
authentication_tech = CONFIG["authentication"]
accumulated_cashback_api = CONFIG["accumulated_cashback_api"]

cashback_user_cases = CashbackAPIUserCases(
    database=database,
    publisher=publisher,
    authentication=authentication_tech,
    accumulated_cashback_api=accumulated_cashback_api,
)
