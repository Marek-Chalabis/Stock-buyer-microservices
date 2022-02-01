from unittest.mock import call

import pytest

from users.models import User
from users.view import RegisterView


class TestRegisterView:
    def test_view_methods(self):
        assert RegisterView.methods == ['GET', 'POST']

    @pytest.mark.parametrize(
        ('tested_form_valid', 'tested_method_call'),
        [
            (False, '_handle_incorrect_form_validation'),
            (True, '_handle_correct_form_validation'),
        ],
    )
    def test_dispatch_request(self, mocker, tested_form_valid, tested_method_call):
        mocker_method_call = mocker.patch(
            f'users.view.RegisterView.{tested_method_call}'
        )
        mocker_register_form = mocker.patch('users.view.RegisterForm')
        mocker_register_form.return_value = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=tested_form_valid),
        )
        RegisterView().dispatch_request()
        mocker_method_call.assert_called_once()

    def test_handle_incorrect_form_validation_errors(self, mocker):
        mocker_flash = mocker.patch('users.view.flash')

        mocker_register_form = mocker.patch('users.view.RegisterForm')

        mocker_register_form.return_value = mocker.Mock(
            errors={
                'test_error1': ['test_error1'],
                'test_error2': ['test_error2'],
            },
        )
        RegisterView()._handle_incorrect_form_validation()

        mocker_flash.assert_has_calls(
            [
                call('test_error1', category='danger'),
                call('test_error2', category='danger'),
            ],
        )

    def test_handle_incorrect_form_validation_template(self, mocker):
        mocker_register_form = mocker.patch('users.view.RegisterForm')
        mocker_form = mocker.Mock(errors=None)
        mocker_register_form.return_value = mocker_form
        mocker_render_template = mocker.patch('users.view.render_template')
        RegisterView()._handle_incorrect_form_validation()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='register.html',
            form=mocker_form,
        )

    def test_handle_correct_form_validation_user_create(self, user, mocker):
        mocker.patch('users.view.RegisterView._get_user_from_form', return_value=user)
        RegisterView()._handle_correct_form_validation()
        assert User.query.get(1) == user

    def test_handle_correct_form_validation_login(self, user, mocker):
        mocker.patch('users.view.RegisterView._get_user_from_form', return_value=user)
        mocker_login_user = mocker.patch('users.view.login_user')
        RegisterView()._handle_correct_form_validation()
        mocker_login_user.assert_called_once_with(user=user)

    def test_handle_correct_form_validation_flash(self, user, mocker):
        mocker.patch('users.view.RegisterView._get_user_from_form', return_value=user)
        mocker_flash = mocker.patch('users.view.flash')
        RegisterView()._handle_correct_form_validation()
        mocker_flash.assert_called_once()

    def test_handle_correct_form_validation_redirect(self, user, mocker):
        mocker.patch('users.view.RegisterView._get_user_from_form', return_value=user)
        mocker_redirect = mocker.patch('users.view.redirect')
        mocker_url_for = mocker.patch('users.view.url_for')
        RegisterView()._handle_correct_form_validation()
        mocker_url_for.assert_called_once_with(endpoint='users.home_page')
        mocker_redirect.assert_called_once_with(location=mocker_url_for())

    def test_get_user_from_form(self, user, mocker):
        mocker_register_form = mocker.patch('users.view.RegisterForm')
        mocker_form = mocker.Mock(
            username=mocker.Mock(data='test_username'),
            email=mocker.Mock(data='test_email'),
            password=mocker.Mock(data='test_password'),
        )
        mocker_register_form.return_value = mocker_form
        tested_user = RegisterView()._get_user_from_form()
        assert tested_user.username == 'test_username'
        assert tested_user.email == 'test_email'
