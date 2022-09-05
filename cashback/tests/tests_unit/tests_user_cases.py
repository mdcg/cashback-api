import unittest
from unittest.mock import MagicMock, Mock

from ddt import ddt, data, unpack
from cashback.domain.exceptions import (
    InvalidCPFException,
    InvalidEmailException,
    InvalidNameException,
    InvalidPasswordException,
    ResellerNotFoundException,
    UnauthorizedException,
)
from cashback.domain.models import Reseller, Sale
from cashback.domain.user_cases import CashbackAPIUserCases


@ddt
class TestUserCases(unittest.TestCase):
    def setUp(self):
        self.database = Mock()
        self.publisher = Mock()
        self.authentication = Mock()
        self.accumulated_cashback_api = Mock()

        self.cashback_user_cases = CashbackAPIUserCases(
            database=self.database,
            publisher=self.publisher,
            authentication=self.authentication,
            accumulated_cashback_api=self.accumulated_cashback_api,
        )

    def test_should_authenticate_user(self):
        self.database.get_reseller_by_email = MagicMock(
            return_value={
                "cpf": "01234567890",
                "password": "d1e8a70b5ccab1dc2f56bbf7e99",
            }
        )
        self.authentication.check_password = MagicMock(return_value=True)
        self.authentication.encode_auth_token = MagicMock(
            return_value="01234567890"
        )
        self.assertEqual(
            self.cashback_user_cases.authenticate_user(
                email="mauro.reseller@cash.com", password="Geek12@"
            ),
            "01234567890",
        )

    def test_should_not_authenticate_when_reseller_not_found(
        self,
    ):
        self.database.get_reseller_by_email = MagicMock(return_value=None)
        with self.assertRaises(ResellerNotFoundException):
            self.cashback_user_cases.authenticate_user(
                email="mauro.reseller@cash.com", password="Geek12@"
            )

        self.authentication.check_password.assert_not_called()
        self.authentication.encode_auth_token.assert_not_called()

    def test_should_not_authenticate_when_reseller_password_is_wrong(
        self,
    ):
        self.database.get_reseller_by_email = MagicMock(
            return_value={
                "cpf": "01234567890",
                "password": "d1e8a70b5ccab1dc2f56bbf7e99",
            }
        )
        self.authentication.check_password = MagicMock(return_value=False)
        with self.assertRaises(UnauthorizedException):
            self.cashback_user_cases.authenticate_user(
                email="mauro.reseller@cash.com", password="Geek12@"
            )

        self.authentication.encode_auth_token.assert_not_called()

    def test_should_extract_reseller_cpf_from_authentication_token(
        self,
    ):
        token = "eyJ0eXAiO.iJKV1QiLCJhbGci.OiJIUzI1NiJ9"
        self.cashback_user_cases.extract_reseller_cpf_from_auth_token(
            token=token
        )
        self.authentication.decode_auth_token.assert_called_with(
            auth_token=token
        )

    def test_should_register_a_reseller(self):
        hashed_password = "d1e8a70b5ccab1dc2f56bbf7e99"
        payload = {
            "cpf": "01234567890",
            "fullname": "Mauro Carvalho",
            "email": "mauro.reselle1r@cash.com",
            "password": "Geek12@",
        }

        self.authentication.hash_password = MagicMock(
            return_value=hashed_password
        )

        self.cashback_user_cases.create_reseller(payload=payload)

        payload["password"] = hashed_password

        self.database.create_reseller.assert_called_with(
            reseller_payload=payload
        )

    def test_should_not_register_reseller_invalid_email(
        self,
    ):
        payload = {
            "cpf": "01234567890",
            "fullname": "Mauro Carvalho",
            "email": "mauro.com",
            "password": "Geek12@",
        }

        with self.assertRaises(InvalidEmailException):
            self.cashback_user_cases.create_reseller(payload=payload)

    def test_should_not_register_reseller_invalid_cpf(self):
        payload = {
            "cpf": "1234567890",
            "fullname": "Mauro Carvalho",
            "email": "mauro.reselle1r@cash.com",
            "password": "Geek12@",
        }

        with self.assertRaises(InvalidCPFException):
            self.cashback_user_cases.create_reseller(payload=payload)

    def test_should_not_register_reseller_invalid_name(
        self,
    ):
        payload = {
            "cpf": "01234567890",
            "fullname": "M4ur0 1337",
            "email": "mauro.reselle1r@cash.com",
            "password": "Geek12@",
        }

        with self.assertRaises(InvalidNameException):
            self.cashback_user_cases.create_reseller(payload=payload)

    def test_should_not_register_reseller_weak_password(
        self,
    ):
        payload = {
            "cpf": "01234567890",
            "fullname": "Mauro Carvalho",
            "email": "mauro.reselle1r@cash.com",
            "password": "123465",
        }

        with self.assertRaises(InvalidPasswordException):
            self.cashback_user_cases.create_reseller(payload=payload)

    def test_should_get_a_reseller(self):
        data = {
            "cpf": "01234567890",
            "fullname": "Mauro Carvalho",
            "email": "mauro.reselle1r@cash.com",
            "password": "d1e8a70b5ccab1dc2f56bbf7e99",
        }

        self.database.get_reseller_by_cpf = MagicMock(return_value=data)
        reseller = self.cashback_user_cases.get_reseller(cpf="01234567890")
        self.assertTrue(isinstance(reseller, Reseller))

    def test_should_raise_exception_when_not_found_reseller(
        self,
    ):
        self.database.get_reseller_by_cpf = MagicMock(return_value=None)
        with self.assertRaises(ResellerNotFoundException):
            self.cashback_user_cases.get_reseller(cpf="01234567890")

    def test_should_create_sale(self):
        payload = {
            "code": "1234516",
            "date": "2022-09-04 19:10:25",
            "value": 1000,
            "reseller_cpf": "01234567890",
        }
        parsed_payload = {
            "code": "1234516",
            "date": "2022-09-04 19:10:25",
            "value": "1000.00",
            "status": "Em validação",
            "reseller_cpf": "01234567890",
        }

        self.cashback_user_cases.get_reseller = MagicMock()
        self.publisher.enqueue = MagicMock()
        self.database.create_sale = MagicMock()

        self.cashback_user_cases.create_sale(payload=payload)

        self.cashback_user_cases.get_reseller.assert_called()
        self.publisher.enqueue.assert_called_with(payload=parsed_payload)
        self.database.create_sale.assert_called_with(
            sale_payload=parsed_payload
        )

    def test_should_not_create_sale_when_reseller_not_found(self):
        payload = {
            "code": "1234516",
            "date": "2022-09-04 19:10:25",
            "value": 1000,
            "reseller_cpf": "01234567890",
        }

        self.cashback_user_cases.get_reseller = MagicMock(
            side_effect=ResellerNotFoundException
        )
        with self.assertRaises(ResellerNotFoundException):
            self.cashback_user_cases.create_sale(payload=payload)

        self.publisher.enqueue.assert_not_called()
        self.database.create_sale.assert_not_called()

    def test_should_get_reseller_sales(self):
        data = [
            {
                "code": "1234516",
                "date": "2022-09-04 19:10:25",
                "value": "1000.00",
                "reseller_cpf": "01234567890",
                "status": "Em validação",
            }
        ]

        self.cashback_user_cases.get_reseller = MagicMock()
        self.database.get_all_sales_from_a_reseller = MagicMock(
            return_value=data
        )

        sales = self.cashback_user_cases.get_reseller_sales(cpf="01234567890")
        self.cashback_user_cases.get_reseller.assert_called()

        self.assertTrue(isinstance(sales, list))
        self.assertTrue(len(sales) == 1)

    def test_should_not_get_reseller_sales_when_reseller_not_found(self):
        self.cashback_user_cases.get_reseller = MagicMock(
            side_effect=ResellerNotFoundException
        )
        with self.assertRaises(ResellerNotFoundException):
            self.cashback_user_cases.get_reseller_sales(cpf="01234567890")

        self.database.get_all_sales_from_a_reseller.assert_not_called()

    @unpack
    @data(
        {
            "sale_value": "100.00",
            "cashback_percentage": "0.10",
            "sale_cashback": "10.00",
        },
        {
            "sale_value": "1400.00",
            "cashback_percentage": "0.15",
            "sale_cashback": "210.00",
        },
        {
            "sale_value": "2100.00",
            "cashback_percentage": "0.20",
            "sale_cashback": "420.00",
        },
    )
    def test_should_get_sales_from_reseller_with_cashback_applied(
        self, sale_value, cashback_percentage, sale_cashback
    ):
        data = [
            {
                "code": "1234516",
                "date": "2022-09-04 19:10:25",
                "reseller_cpf": "01234567890",
                "status": "Aprovado",
                "value": sale_value,
            }
        ]
        parsed_data_with_cashback = {
            "cashback_percentage": cashback_percentage,
            "sales": [
                {
                    "code": "1234516",
                    "date": "2022-09-04 19:10:25",
                    "status": "Aprovado",
                    "value": sale_value,
                    "cashback": sale_cashback,
                }
            ],
        }
        self.cashback_user_cases.get_reseller = MagicMock()
        self.database.get_all_sales_from_a_reseller_from_current_month = (
            MagicMock(return_value=data)
        )
        sales_with_cashback = self.cashback_user_cases.get_sales_from_reseller_with_cashback_applied(
            cpf="01234567890"
        )

        self.assertEqual(
            sales_with_cashback,
            parsed_data_with_cashback,
        )

    def test_should_not_get_sales_from_reseller_with_cashback_applied_when_reseller_not_found(
        self,
    ):
        self.cashback_user_cases.get_reseller = MagicMock(
            side_effect=ResellerNotFoundException
        )
        with self.assertRaises(ResellerNotFoundException):
            self.cashback_user_cases.get_sales_from_reseller_with_cashback_applied(
                cpf="01234567890"
            )

        self.database.get_all_sales_from_a_reseller_from_current_month.assert_not_called()

    def test_should_get_reseller_accumulated_cashback(self):
        reseller_cpf = "01234567890"
        self.cashback_user_cases.get_reseller_accumulated_cashback(
            cpf=reseller_cpf
        )
        self.accumulated_cashback_api.check_accumulated_cashback_from_a_reseller.assert_called_with(
            reseller_cpf=reseller_cpf
        )
