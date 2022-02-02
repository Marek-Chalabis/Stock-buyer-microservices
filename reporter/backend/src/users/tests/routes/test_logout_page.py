from http import HTTPStatus

from users.routes import logout_page


def test_register_page_status(client):
    response = client.get('/logout')
    assert response.status_code == HTTPStatus.FOUND


def test_register_page_logout(mocker):
    mocker_logout_user = mocker.patch('users.routes.logout_user')
    logout_page()
    mocker_logout_user.assert_called_once_with()


def test_register_page_flash(mocker):
    mocker_flash = mocker.patch('users.routes.flash')
    logout_page()
    mocker_flash.assert_called_once()


def test_register_page_redirect(mocker):
    mocker_redirect = mocker.patch('users.routes.redirect')
    mocker_url_for = mocker.patch('users.routes.url_for')
    logout_page()
    mocker_url_for.assert_called_once_with(endpoint='users.home_page')
    mocker_redirect.assert_called_once_with(location=mocker_url_for())
