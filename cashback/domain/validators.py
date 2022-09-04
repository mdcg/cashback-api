import re

from cashback.domain.exceptions import (
    InvalidCPFException,
    InvalidEmailException,
    InvalidNameException,
    InvalidPasswordException,
)


class Validator:
    @staticmethod
    def validate_fullname(fullname):
        regex = re.compile("[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ\s]+$")
        if not bool(re.fullmatch(regex, fullname)):
            raise InvalidNameException()

    @staticmethod
    def validate_email(email):
        regex = re.compile(
            "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        if not bool(re.fullmatch(regex, email)):
            raise InvalidEmailException()

    @staticmethod
    def validate_password(password):
        regex = re.compile(
            "^(?=.*[a-zç])(?=.*[A-ZÇ])(?=.*\d)(?=.*[@$!%*#?&\-])[A-Za-zçÇ\d@$!#%*?&\-]{6,20}$"
        )
        if not bool(re.search(regex, password)):
            raise InvalidPasswordException()

    @staticmethod
    def validate_cpf(cpf):
        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            raise InvalidCPFException()

        # Validação do primeiro dígito verificador:
        sum_of_products = sum(
            a * b for a, b in zip(numbers[0:9], range(10, 1, -1))
        )
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            raise InvalidCPFException()

        # Validação do segundo dígito verificador:
        sum_of_products = sum(
            a * b for a, b in zip(numbers[0:10], range(11, 1, -1))
        )
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            raise InvalidCPFException()
