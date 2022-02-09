from http import HTTPStatus

import pytest

from users.routes import (
    home_page,
    load_user,
    logout_page,
)


@pytest.mark.parametrize(
    'tested_endpoint',
    [
        '/',
        '/home',
    ],
)
def test_home_page_status(client, tested_endpoint):
    response = client.get(tested_endpoint)
    assert response.status_code == HTTPStatus.OK


def test_home_page_rendered_template(mocker):
    mocker_render_template = mocker.patch('users.routes.render_template')
    home_page()
    mocker_render_template.assert_called_once_with(template_name_or_list='home.html')


def test_load_user_user_exists(db, user):
    db.session.add(user)
    assert load_user('1') == user


def test_load_user_user_not_exists():
    assert not load_user('1')


def test_login_page_status(client):
    response = client.get('/login')
    assert response.status_code == HTTPStatus.OK


def test_logout_page_status(client):
    response = client.get('/logout')
    assert response.status_code == HTTPStatus.FOUND


def test_logout_page_logout(mocker):
    mocker_logout_user = mocker.patch('users.routes.logout_user')
    logout_page()
    mocker_logout_user.assert_called_once_with()


def test_logout_page_flash(mocker):
    mocker_flash = mocker.patch('users.routes.flash')
    logout_page()
    mocker_flash.assert_called_once()


def test_logout_page_redirect(mocker):
    mocker_redirect = mocker.patch('users.routes.redirect')
    mocker_url_for = mocker.patch('users.routes.url_for')
    logout_page()
    mocker_url_for.assert_called_once_with(endpoint='users.home_page')
    mocker_redirect.assert_called_once_with(location=mocker_url_for())


def test_profile_page_status(client):
    response = client.get('/profile')
    assert response.status_code == HTTPStatus.FOUND


def test_register_page_status(client):
    response = client.get('/register')
    assert response.status_code == HTTPStatus.OK
