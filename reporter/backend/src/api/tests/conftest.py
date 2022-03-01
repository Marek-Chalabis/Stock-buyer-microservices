from typing import Dict

import pytest

from src.api.v1.typing import STOCKS


@pytest.fixture
def token_header(mocker) -> Dict[str, str]:
    mocker_token = 'mocker_x-api-key'
    mocker.patch('src.api.security.request.headers.get', return_value=mocker_token)
    mocker.patch(
        'src.api.security.BaseConfig.SECRET_KEY',
        new_callable=mocker.PropertyMock,
        return_value=mocker_token,
    )
    return {'x-api-key': mocker_token}


@pytest.fixture
def stocks() -> STOCKS:
    return {
        'stocks': [
            {
                'name': 'test_name_1',
                'symbol': 'T1',
                'price': 10.10,
                'quantity': 1,
            },
            {
                'name': 'test_name_2',
                'symbol': 'T2',
                'price': 20.20,
                'quantity': 2,
            },
        ]
    }
