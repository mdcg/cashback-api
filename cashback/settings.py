from os import getenv

from cashback.adapters.authentication.jwt import JWTAuthenticationAdapter
from cashback.adapters.databases.inmemory import InMemoryAdapter
from cashback.adapters.databases.postgresql import PostgreSQLAdapter
from cashback.adapters.external_apis.restful_request import (
    RestfulRequestAdapter,
)

AUTOMATIC_APPROVED_RESELLERS_CPFS = getenv(
    "AUTOMATIC_APPROVED_RESELLERS_CPFS", "153.509.460-56"
).split(",")

DATABASE = getenv("DATABASE", "postgresql")

ACCUMULATED_CASHBACK_API_COMMUNICATION = getenv("DATABASE", "restful")

AUTHENTICATION = getenv("AUTHENTICATION", "jwt")

DATABASE_IMPLEMENTATIONS = {
    "inmemory": InMemoryAdapter,
    "postgresql": PostgreSQLAdapter,
}

ACCUMULATED_CASHBACK_API_IMPLEMENTATIONS = {
    "restful": RestfulRequestAdapter,
}

AUTHENTICATION_TECHNOLOGIES_IMPLEMENTATIONS = {
    "jwt": JWTAuthenticationAdapter,
}

CONFIG = {
    "database": DATABASE_IMPLEMENTATIONS.get(DATABASE, "postgresql"),
    "accumulated_cashback_api": ACCUMULATED_CASHBACK_API_IMPLEMENTATIONS.get(
        ACCUMULATED_CASHBACK_API_COMMUNICATION, "restful"
    ),
    "authentication": AUTHENTICATION_TECHNOLOGIES_IMPLEMENTATIONS.get(
        AUTHENTICATION, "jwt"
    ),
}
