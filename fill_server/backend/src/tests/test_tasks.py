from src.celery import send_trade_fill_to_controller


def test_send_trade_fill_to_controller_fill_call(mocker):
    mocker_get_random_fill = mocker.patch('src.celery.get_random_fill')
    mocker.patch('src.celery.httpx.post')
    send_trade_fill_to_controller()
    mocker_get_random_fill.assert_called_once_with()


def test_send_trade_fill_to_controller_request(mocker):
    mocker_setting = mocker.patch('src.celery.settings')
    mocker_setting.CONTROLLER_SERVER_KEY_SECRET = 'test_secret'
    mocker_setting.CONTROLLER_SERVER_CLIENT = {'trade-fills': 'test_url'}
    mocker.patch('src.celery.get_random_fill', return_value={'test': 'test'})
    mocker_post = mocker.patch('src.celery.httpx.post')
    send_trade_fill_to_controller()
    mocker_post.assert_called_once_with(
        'test_url',
        json={'test': 'test'},
        headers={'x-api-key': 'test_secret'},
    )
