from src.periodic_tasks.tasks import send_account_split_to_controller


def test_send_account_split_to_controller(mocker):
    mocker_get_random_account_split_data = mocker.patch(
        'src.accounts.account_split_data.AccountsSplitData.'
        + 'get_random_account_split_data',
    )
    send_account_split_to_controller()
    mocker_get_random_account_split_data.assert_called_once()
