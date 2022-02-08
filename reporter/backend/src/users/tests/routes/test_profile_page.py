from http import HTTPStatus


def test_profile_page_status(client):
    response = client.get('/profile')
    assert response.status_code == HTTPStatus.FOUND
