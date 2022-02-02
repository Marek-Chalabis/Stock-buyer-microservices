import pytest
import wtforms

from users.forms import RegisterForm


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
