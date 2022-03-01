import pytest

from src.users.view import (
    LoginView,
    RegisterView,
)


class TestLoginView:
    def test_view_methods(self):
        assert RegisterView.methods == ['GET', 'POST']

    @pytest.fixture
    def login_form(self, mocker):
        return mocker.patch(
            'src.users.view.LoginForm',
            return_value=mocker.Mock(
                validate_on_submit=mocker.Mock(return_value=True),
                username=mocker.Mock(data='test_username'),
                password=mocker.Mock(data='test_password'),
            ),
        )

    def test_dispatch_request_valid(self, mocker, login_form):
        mocker_get_user_from_form = mocker.patch(
            'src.users.view.LoginView._get_user_from_form',
        )
        mocker_handle_correct_user = mocker.patch(
            'src.users.view.LoginView._handle_correct_user',
        )
        LoginView().dispatch_request()
        mocker_handle_correct_user.assert_called_once_with(
            user=mocker_get_user_from_form(),
        )

    def test_dispatch_request_invalid_password(
        self,
        mocker,
        login_form,
    ):
        mocker.patch(
            'src.users.view.LoginView._get_user_from_form',
            return_value=mocker.Mock(
                verify_password=mocker.Mock(return_value=False),
            ),
        )
        mocker_flash = mocker.patch('src.users.view.flash')
        mocker_render_template = mocker.patch('src.users.view.render_template')
        LoginView().dispatch_request()
        mocker_flash.assert_called_once()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='login.html',
            form=login_form.return_value,
        )

    def test_dispatch_request_valid_form_invalid_user(self, mocker, login_form):
        mocker.patch('src.users.view.LoginView._get_user_from_form', return_value=None)
        mocker_flash = mocker.patch('src.users.view.flash')
        mocker_render_template = mocker.patch('src.users.view.render_template')
        LoginView().dispatch_request()
        mocker_flash.assert_called_once()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='login.html',
            form=login_form.return_value,
        )

    def test_dispatch_request_invalid_form(self, mocker):
        mocker_login_form = mocker.patch('src.users.view.LoginForm')
        mocker_form = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=False),
        )
        mocker_login_form.return_value = mocker_form
        mocker_render_template = mocker.patch('src.users.view.render_template')
        LoginView().dispatch_request()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='login.html',
            form=mocker_login_form.return_value,
        )

    def test_handle_correct_user_login_user(self, mocker, user):
        mocker_login_user = mocker.patch('src.users.view.login_user')
        LoginView()._handle_correct_user(user=user)
        mocker_login_user.assert_called_once_with(user=user)

    def test_handle_correct_user_flash(self, mocker, user):
        mocker.patch('src.users.view.login_user')
        mocker_flash = mocker.patch('src.users.view.flash')
        LoginView()._handle_correct_user(user=user)
        mocker_flash.assert_called_once()

    def test_handle_correct_user_redirect(self, mocker, user):
        mocker_redirect = mocker.patch('src.users.view.redirect')
        mocker_url_for = mocker.patch('src.users.view.url_for')
        LoginView()._handle_correct_user(user=user)
        mocker_url_for.assert_called_once_with(endpoint='trades.trades_page')
        mocker_redirect.assert_called_once_with(location=mocker_url_for())

    def test_get_user_from_form_user_exists(self, mocker, user_in_db):
        mocker_login_form = mocker.patch('src.users.view.LoginForm')
        mocker_login_form.return_value = mocker.Mock(
            username=mocker.Mock(data='test_username'),
        )
        assert LoginView()._get_user_from_form() == user_in_db
