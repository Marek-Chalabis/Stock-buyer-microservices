from decimal import Decimal

import pytest

from app import db


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


class TestUserProfile:
    @pytest.mark.parametrize(
        (
            'tested_amount',
            'tested_commit',
            'expected_result',
        ),
        [
            (Decimal(100), True, '$100.00'),
            (Decimal(-100), True, '-$100.00'),
            (Decimal(100), False, Decimal(100)),
        ],
    )
    def test_update_money_by_amount(
        self,
        user_in_db,
        tested_amount,
        tested_commit,
        expected_result,
    ):
        user_in_db.user_profile.update_money_by_amount(
            amount=tested_amount,
            commit=tested_commit,
        )
        assert tested_commit != (user_in_db.user_profile in db.session.dirty)
        assert user_in_db.user_profile.money == expected_result
