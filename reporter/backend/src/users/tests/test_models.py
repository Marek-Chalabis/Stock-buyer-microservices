import pytest


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
