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

DATABASE = getenv("DATABASE", "inmemory")

EXTERNAL_API_COMMUNICATION = getenv("DATABASE", "restful")

AUTHENTICATION = getenv("AUTHENTICATION", "jwt")

# Esse valor é usado para determinar a complexidade da criptografia, consulte
# bcrypt para obter mais detalhes.
BCRYPT_LOG_ROUNDS = 13

SECRET_KEY = getenv("SECRET_KEY", "super_secret")

AVAILABLE_DATABASE_IMPLEMENTATIONS = {
    "inmemory": InMemoryAdapter,
    "postgresql": PostgreSQLAdapter,
}

AVAILABLE_EXTERNAL_API_IMPLEMENTATIONS = {
    "restful": RestfulRequestAdapter,
}

AVAILABLE_AUTHENTICATION_IMPLEMENTATIONS = {
    "jwt": JWTAuthenticationAdapter,
}

CONFIG = {
    "database": AVAILABLE_DATABASE_IMPLEMENTATIONS.get(DATABASE, "inmemory"),
    "external_api_communication": AVAILABLE_EXTERNAL_API_IMPLEMENTATIONS.get(
        EXTERNAL_API_COMMUNICATION, "restful"
    ),
    "authentication": AVAILABLE_AUTHENTICATION_IMPLEMENTATIONS.get(
        AUTHENTICATION, "jwt"
    ),
}

# /*                    */
# /* Adapters Settings  */
# /*                    */

POSTGRESQL_URI = getenv("POSTGRESQL_URI")

EXTERNAL_CASHBACK_RESTFUL_API_URL = getenv(
    "EXTERNAL_CASHBACK_RESTFUL_API_URL",
    "https://mdaqk8ek5j.execute-api.us-east1.amazonaws.com/v1/cashback",
)
