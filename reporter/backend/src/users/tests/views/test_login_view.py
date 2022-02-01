from users.view import (
    LoginView,
    RegisterView,
)


class TestLoginView:
    def test_view_methods(self):
        assert RegisterView.methods == ['GET', 'POST']

    def test_dispatch_request_invalid_form(self, mocker):
        mocker_render_handle_correct_form_validation = mocker.patch(
            'users.view.LoginView._handle_correct_form_validation'
        )
        mocker_login_form = mocker.patch('users.view.LoginForm')
        mocker_login_form.return_value = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=True),
        )
        LoginView().dispatch_request()
        mocker_render_handle_correct_form_validation.assert_called_once_with()

    def test_dispatch_request_valid_form(self, mocker):
        mocker_render_template = mocker.patch(f'users.view.render_template')
        mocker_login_form = mocker.patch('users.view.LoginForm')
        mocker_login_form.return_value = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=False),
        )
        LoginView().dispatch_request()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='login.html', form=mocker_login_form()
        )

    def test_get_user_from_form_user_exists(self, mocker, user_in_db):
        mocker_login_form = mocker.patch('users.view.LoginForm')
        mocker_login_form.return_value = mocker.Mock(
            username=mocker.Mock(data='test_username'),
        )
        assert LoginView()._get_user_from_form() == user_in_db

    def test_get_user_from_form_user_does_not_exists(self, mocker, user_in_db):
        mocker_login_form = mocker.patch('users.view.LoginForm')
        mocker_login_form.return_value = mocker.Mock(
            username=mocker.Mock(data='test_username_nope'),
        )
        assert not LoginView()._get_user_from_form()

    def test_handle_correct_form_validation_no_user(self, mocker):
        mocker.patch('users.view.LoginView._get_user_from_form', return_value=None)
        mocker_handle_incorrect_user = mocker.patch(
            'users.view.LoginView._handle_incorrect_user'
        )
        LoginView()._handle_correct_form_validation()
        mocker_handle_incorrect_user.assert_called_once_with()

    def test_handle_correct_form_validation_wrong_pass(self, mocker):
        mocker_user = mocker.Mock(
            verify_password=mocker.Mock(return_value=False),
        )
        mocker.patch(
            'users.view.LoginView._get_user_from_form', return_value=mocker_user
        )
        mocker_handle_incorrect_user = mocker.patch(
            'users.view.LoginView._handle_incorrect_user'
        )
        LoginView()._handle_correct_form_validation()
        mocker_handle_incorrect_user.assert_called_once_with()

    def test_handle_correct_form_validation_accept(self, mocker):
        mocker_user = mocker.Mock(
            verify_password=mocker.Mock(return_value=True),
        )
        mocker.patch(
            'users.view.LoginView._get_user_from_form', return_value=mocker_user
        )
        mocker_handle_correct_user = mocker.patch(
            'users.view.LoginView._handle_correct_user'
        )
        LoginView()._handle_correct_form_validation()
        mocker_handle_correct_user.assert_called_once_with(user=mocker_user)

    def test_handle_correct_user_flash(self, mocker, user):
        mocker_flash = mocker.patch('users.view.flash')
        LoginView()._handle_correct_user(user=user)
        mocker_flash.assert_called_once()

    def test_handle_correct_user_login_user(self, mocker, user):
        mocker_login_user = mocker.patch('users.view.login_user')
        LoginView()._handle_correct_user(user=user)
        mocker_login_user.assert_called_once_with(user=user)

    def test_handle_correct_user_redirect(self, mocker, user):
        mocker_redirect = mocker.patch('users.view.redirect')
        mocker_url_for = mocker.patch('users.view.url_for')
        LoginView()._handle_correct_user(user=user)
        mocker_url_for.assert_called_once_with(endpoint='users.home_page')
        mocker_redirect.assert_called_once_with(location=mocker_url_for())

    def test_handle_incorrect_user_flash(self, mocker):
        mocker_flash = mocker.patch('users.view.flash')
        LoginView()._handle_incorrect_user()
        mocker_flash.assert_called_once()

    def test_handle_incorrect_user_render_template(self, mocker):
        mocker_render_template = mocker.patch(f'users.view.render_template')
        mocker_login_form = mocker.patch('users.view.LoginForm')
        LoginView()._handle_incorrect_user()
        mocker_render_template.assert_called_once_with(
            template_name_or_list='login.html', form=mocker_login_form()
        )
