from src.celery import (
    CONTROLLER_SERVER_CLIENT,
    send_trade_fill_to_controller,
)


def test_send_trade_fill_to_controller_random_fill_called(mocker):
    mocker_get_random_fill = mocker.patch('src.celery.get_random_fill')
    mocker.patch('src.celery.httpx.post')
    send_trade_fill_to_controller()
    mocker_get_random_fill.assert_called_once_with()


def test_send_trade_fill_to_controller_request(mocker):
    mocker_key = mocker.patch('src.celery.CONTROLLER_SERVER_KEY_SECRET')
    mocker.patch.dict(CONTROLLER_SERVER_CLIENT, {'fills': 'test_url'})
    mocker.patch('src.celery.get_random_fill', return_value={'test': 'test'})
    mocker_post = mocker.patch('src.celery.httpx.post')
    send_trade_fill_to_controller()
    mocker_post.assert_called_once_with(
        'test_url', json={'test': 'test'}, headers={'x-api-key': mocker_key}
    )
