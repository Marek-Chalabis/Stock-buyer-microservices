from fastapi import status
from fastapi.testclient import TestClient

from src.api.api_v1.api import authorizer
from src.main import app

client = TestClient(app)

app.dependency_overrides[authorizer] = lambda: None


def test_splits_accounts(mocker):
    mocker_set = mocker.patch('src.api.api_v1.endpoints.account_split.redis.set')
    response = client.post('/api/v1/accounts-splits/', json={'test': 1})
    assert response.status_code == status.HTTP_202_ACCEPTED
    mocker_set.assert_called_once_with('accounts_splits', '{"test": 1.0}')
