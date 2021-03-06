import pytest

from src.users.view import RegisterView


class TestRegisterView:
    def test_view_methods(self):
        assert RegisterView.methods == ['GET', 'POST']

    @pytest.fixture
    def register_form(self, mocker):
        return mocker.patch(
            'src.users.view.RegisterForm',
            return_value=mocker.Mock(
                validate_on_submit=mocker.Mock(return_value=False),
                username=mocker.Mock(data='test_username'),
                email=mocker.Mock(data='test_email'),
                password=mocker.Mock(data='test_password'),
            ),
        )

    def test_dispatch_request_validate_correct(self, mocker):
        mocker_handle_correct_register_form = mocker.patch(
            'src.users.view.RegisterView._handle_correct_register_form',
        )
        mocker_register_form = mocker.patch('src.users.view.RegisterForm')
        mocker_register_form.return_value = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=True),
        )
        RegisterView().dispatch_request()
        mocker_handle_correct_register_form.assert_called_once_with()

    def test_dispatch_request_validate_incorrect(self, mocker, register_form):
        mocker.patch('src.users.view.flash_errors_from_form')
        mocker_render_template = mocker.patch('src.users.view.render_template')
        RegisterView().dispatch_request()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='register.html',
            form=register_form.return_value,
        )

    def test_dispatch_request_flash_errors(self, mocker, register_form):
        mocker_flash_errors_from_form = mocker.patch(
            'src.users.view.flash_errors_from_form',
        )
        RegisterView().dispatch_request()
        mocker_flash_errors_from_form.assert_called_once_with(
            form=register_form.return_value,
        )

    def test_handle_correct_register_form_user_save(self, mocker, register_form):
        mocker_save = mocker.patch('src.users.view.User.save')
        RegisterView()._handle_correct_register_form()
        mocker_save.assert_called_once_with()

    def test_handle_correct_register_form_redirect(self, mocker, register_form):
        mocker.patch('src.users.view.User.save')
        mocker_flash = mocker.patch('src.users.view.flash')
        RegisterView()._handle_correct_register_form()
        mocker_flash.assert_called_once()

    def test_handle_correct_register_form_flash(self, mocker, register_form):
        mocker.patch('src.users.view.User.save')
        mocker_redirect = mocker.patch('src.users.view.redirect')
        mocker_url_for = mocker.patch('src.users.view.url_for')
        RegisterView()._handle_correct_register_form()
        mocker_url_for.assert_called_once_with(endpoint='trades.trades_page')
        mocker_redirect.assert_called_once_with(location=mocker_url_for())
