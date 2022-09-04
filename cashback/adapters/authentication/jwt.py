from datetime import datetime, timedelta
from os import getenv

import bcrypt
from cashback.domain.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
)
from cashback.ports.authentication import AuthenticationPort

import jwt

SECRET_KEY = getenv("SECRET_KEY", "super_secret")


class JWTAuthenticationAdapter(AuthenticationPort):
    @staticmethod
    def hash_password(password):
        bytepasswd = password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password=bytepasswd, salt=salt).decode()

    @staticmethod
    def check_password(hashed_password, password):
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8"),
        )

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                jwt=auth_token, key=SECRET_KEY, algorithms="HS256"
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()

        return payload["sub"]

    @staticmethod
    def encode_auth_token(reseller_cpf):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, hours=8),
            "iat": datetime.utcnow(),
            "sub": reseller_cpf,
        }

        return jwt.encode(paylod=payload, key=SECRET_KEY, algorithm="HS256")
