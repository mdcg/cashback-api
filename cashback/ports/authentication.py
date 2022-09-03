from abc import ABC, abstractmethod


class AuthenticationPort(ABC):
    @abstractmethod
    def hash_password(self, password):
        pass

    @abstractmethod
    def check_password(self, hashed_password, password):
        pass

    @staticmethod
    @abstractmethod
    def decode_auth_token(auth_token):
        pass

    @staticmethod
    @abstractmethod
    def encode_auth_token(reseller_cpf):
        pass
