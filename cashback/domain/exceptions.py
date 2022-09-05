class ResellerNotFoundException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class InvalidNameException(Exception):
    pass


class InvalidEmailException(Exception):
    pass


class InvalidPasswordException(Exception):
    pass


class InvalidCPFException(Exception):
    pass


class ResellerAlreadyRegistedException(Exception):
    pass


class SaleAlreadyRegistedException(Exception):
    pass


class SaleDatetimeFormatException(Exception):
    pass


class TokenExpiredException(Exception):
    pass


class InvalidTokenException(Exception):
    pass
