from decimal import Decimal

import pytest

from app import db
from users.enums import MoneyOperation
from users.models import User


class TestUsers:
    def test_password_hash(self, user_in_db):
        assert user_in_db.password_hash != 'test_password_hash'

    @pytest.mark.parametrize(
        ('tested_password', 'expected_result'),
        [
            ('test_password', True),
            ('different_password', False),
        ],
    )
    def test_verify_password(self, user_in_db, tested_password, expected_result):
        assert user_in_db.verify_password(tested_password) == expected_result

    def test_create(self):
        tested_username = 'test_username'
        tested_email = 'test_email'
        tested_user_from_create = User.create(
            username=tested_username,
            email=tested_email,
            password='test_password',
        )
        tested_user_from_db = db.session.query(User).first()
        assert tested_user_from_db.username == tested_user_from_create.username
        assert tested_user_from_db.email == tested_user_from_create.email


class TestUserProfile:
    def test_user_profile_relationship(self, user_in_db):
        assert user_in_db.user_profile
        assert user_in_db.user_profile.user == user_in_db

    def test_money_in_decimal(self, user_in_db):
        assert user_in_db.user_profile.money_in_decimal == Decimal(0)

    @pytest.mark.parametrize(
        ('tested_operation', 'expected_result'),
        [
            (MoneyOperation.DEPOSIT, '$100.00'),
            (MoneyOperation.PAY_OUT, '-$100.00'),
        ],
    )
    def test_change_money_based_on_operation(
        self,
        user_in_db,
        tested_operation,
        expected_result,
    ):
        user_in_db.user_profile.change_money_based_on_operation(
            amount=Decimal(100),
            operation=tested_operation.value,
        )
        assert user_in_db.user_profile.money == expected_result
