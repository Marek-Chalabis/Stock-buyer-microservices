from fastapi import (
    Depends,
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

from src.api.authorize import AuthorizerDependencyByXApiKey

authorizer = AuthorizerDependencyByXApiKey()
app = FastAPI(dependencies=[Depends(authorizer)])


@app.get('/')
def test_endpoint():
    return 'test'


client = TestClient(app)


def test_unauthorized_no_api_key_header():
    response = client.get('/')
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_unauthorized_wrong_header_value(mocker):
    mocker_settings = mocker.patch('src.api.authorize.settings')
    mocker_settings.X_API_KEY_SECRET = 'foo'
    response = client.get('/', headers={'x-api-key': 'bar'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authorized(mocker):
    mocker_settings = mocker.patch('src.api.authorize.settings')
    mocker_settings.X_API_KEY_SECRET = 'test'
    response = client.get('/', headers={'x-api-key': 'test'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 'test'
