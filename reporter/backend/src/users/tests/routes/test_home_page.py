from http import HTTPStatus

import pytest

from users.routes import home_page


@pytest.mark.parametrize(
    'tested_endpoint',
    [
        '/',
        '/home',
    ],
)
def test_home_page_status(app_client, tested_endpoint):
    response = app_client.get(tested_endpoint)
    assert response.status_code == HTTPStatus.OK


def test_home_page_rendered_template(mocker):
    mocker_render_template = mocker.patch('users.routes.render_template')
    home_page()
    mocker_render_template.assert_called_once_with(template_name_or_list='home.html')
