from decimal import Decimal

import pytest
import wtforms

from flask_login import login_user

from users.enums import MoneyOperation
from users.forms import (
    MoneyForm,
    RegisterForm,
)


class TestRegisterForm:
    def test_validate_username_no_username(self, mocker, user_in_db):
        mock_username = mocker.Mock(data='username_that_does_not_exists')
        assert not RegisterForm().validate_username(mock_username)

    def test_validate_username_username_exists(self, mocker, user_in_db):
        mock_username = mocker.Mock(data='test_username')
        with pytest.raises(wtforms.validators.ValidationError):
            RegisterForm().validate_username(mock_username)

    def test_validate_email_no_email(self, mocker, user_in_db):
        mock_email = mocker.Mock(data='email_that_does_not_exists')
        assert not RegisterForm().validate_email(mock_email)

    def test_validate_email_email_exists(self, mocker, user_in_db):
        mock_email = mocker.Mock(data='test_email')
        with pytest.raises(wtforms.validators.ValidationError):
            RegisterForm().validate_email(mock_email)


class TestMoneyForm:
    def test_validate_amount_over_account_money(self, mocker, user_in_db):
        mocker.Mock(
            data='users.forms.flask_login.current_user',
            return_value=user_in_db,
        )
        mocker.patch(
            'users.forms.MoneyForm.data',
            new_callable=mocker.PropertyMock,
            return_value={'operation': MoneyOperation.PAY_OUT},
        )
        login_user(user_in_db)
        mock_amount = mocker.Mock(data=Decimal(1))
        money_form = MoneyForm()
        with pytest.raises(wtforms.validators.ValidationError):
            money_form.validate_amount(mock_amount)
