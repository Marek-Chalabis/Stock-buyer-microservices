import pytest
import wtforms

from users.forms import (
    LoginForm,
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


class TestLoginForm:
    def test_validate_username_no_user(self, mocker):
        mock_username = mocker.Mock(data='username_that_does_not_exists')
        with pytest.raises(wtforms.validators.ValidationError):
            LoginForm().validate_username(mock_username)

    def test_validate_password_wrong_password(self, mocker, user_in_db):
        mocker.patch('users.forms.User.get_user_by_username', return_value=user_in_db)
        mock_password = mocker.Mock(data='wrong_password')
        with pytest.raises(wtforms.validators.ValidationError):
            LoginForm().validate_password(mock_password)
