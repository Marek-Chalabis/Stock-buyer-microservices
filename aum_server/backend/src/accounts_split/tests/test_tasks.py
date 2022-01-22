from src.accounts_split.tasks import send_accounts_splits_to_controller


def test_send_accounts_splits_to_controller_split(mocker):
    mocker_get_random_accounts_splits_data = mocker.patch(
        'src.accounts_split.accounts.AccountsSplits.get_random_accounts_splits',
        return_value={},
    )
    mocker.patch('src.accounts_split.tasks.httpx.post')
    send_accounts_splits_to_controller()
    mocker_get_random_accounts_splits_data.assert_called_once()


def test_send_accounts_splits_request(mocker):
    mocker_setting = mocker.patch('src.accounts_split.tasks.settings')
    mocker_setting.CONTROLLER_SERVER_KEY_SECRET = 'test_secret'
    mocker_setting.CONTROLLER_SERVER_CLIENT = {'accounts-splits': 'test_url'}
    mocker.patch(
        'src.accounts_split.accounts.AccountsSplits.get_random_accounts_splits',
        return_value={'test': 'test'},
    )
    mocker_httpx_post = mocker.patch('src.accounts_split.tasks.httpx.post')
    send_accounts_splits_to_controller()
    mocker_httpx_post.assert_called_once_with(
        'test_url',
        json={'test': 'test'},
        headers={'x-api-key': 'test_secret'},
    )
