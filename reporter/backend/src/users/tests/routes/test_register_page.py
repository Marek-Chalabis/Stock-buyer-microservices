from http import HTTPStatus


def test_register_page_status(client):
    response = client.get('/register')
    assert response.status_code == HTTPStatus.OK