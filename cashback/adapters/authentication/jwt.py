from datetime import datetime, timedelta

import bcrypt
from cashback.ports.authentication import AuthenticationPort
from cashback.settings import BCRYPT_LOG_ROUNDS, SECRET_KEY

import jwt


class JWTAuthenticationAdapter(AuthenticationPort):
    def hash_password(self, password):
        return bcrypt.generate_password_hash(
            password, BCRYPT_LOG_ROUNDS
        ).decode()

    def check_password(self, hashed_password, password):
        return bcrypt.check_password_hash(hashed_password, password)

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

        return payload["sub"]

    @staticmethod
    def encode_auth_token(reseller_cpf):
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=0, hours=8),
                "iat": datetime.utcnow(),
                "sub": reseller_cpf,
            }
        except Exception as e:
            return e

        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
