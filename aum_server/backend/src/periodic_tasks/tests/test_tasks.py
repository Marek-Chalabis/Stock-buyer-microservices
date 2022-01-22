import os

from src.controller_server_endpoints import CONTROLLER_SERVER_CLIENT
from src.periodic_tasks.tasks import send_account_split_to_controller


def test_send_account_split_to_controller_split(mocker):
    mocker_get_random_account_split_data = mocker.patch(
        'src.accounts.account_split_data.AccountsSplitData.'
        + 'get_random_account_split_data',
        return_value={'test': 'test'},
    )
    send_account_split_to_controller()
    mocker_get_random_account_split_data.assert_called_once()


def test_send_account_split_to_controller_request(mocker):
    mocker_secret_key = mocker.patch(
        'src.periodic_tasks.tasks.CONTROLLER_SERVER_KEY_SECRET',
    )
    mocker.patch.dict(CONTROLLER_SERVER_CLIENT, {'account-split': 'test_url'})
    mocker.patch(
        'src.accounts.account_split_data.AccountsSplitData.'
        + 'get_random_account_split_data',
        return_value={'test': 'test'},
    )
    mocker_httpx_post = mocker.patch('src.periodic_tasks.tasks.httpx.post')
    send_account_split_to_controller()
    mocker_httpx_post.assert_called_once_with(
        'test_url',
        json={'test': 'test'},
        headers={'x-api-key': mocker_secret_key},
    )
