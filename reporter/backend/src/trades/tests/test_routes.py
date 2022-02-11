from http import HTTPStatus


def test_logout_page_status(client):
    response = client.get('/trades')
    assert response.status_code == HTTPStatus.FOUND
