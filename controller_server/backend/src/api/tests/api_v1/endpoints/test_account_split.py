from fastapi import status
from fastapi.testclient import TestClient

from src.api.api_v1.api import authorizer
from src.main import app

client = TestClient(app)

app.dependency_overrides[authorizer] = lambda: None


def test_splits_accounts(mocker):
    mocker_hmset = mocker.patch('src.api.api_v1.endpoints.account_split.redis.hmset')
    response = client.post('/api/v1/account-split/', json={'test': 1})
    assert response.status_code == status.HTTP_202_ACCEPTED
    mocker_hmset.assert_called_once_with('accounts_split_data', {'test': 1.0})
