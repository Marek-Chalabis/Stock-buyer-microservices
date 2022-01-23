from src.orders.tasks import send_stock_purchase_order_to_reporter


def test_send_stock_purchase_order_to_reporter_order(mocker):
    tested_trade_fill = {'test': 1}
    mocker_get_random_accounts_splits_data = mocker.patch(
        'src.orders.tasks.StockPurchaseOrder.prepare_stock_purchase_order',
    )
    mocker.patch('src.orders.tasks.httpx.post')
    send_stock_purchase_order_to_reporter(tested_trade_fill)
    mocker_get_random_accounts_splits_data.assert_called_once_with()


def test_send_stock_purchase_order_to_reporter_post(mocker):
    mocker_setting = mocker.patch('src.orders.tasks.settings')
    mocker_setting.REPORTER_SERVER_KEY_SECRET = 'test_secret'
    mocker_setting.reporter_server_client = {'stocks-purchase-orders': 'test_url'}
    mocker_get_random_accounts_splits_data = mocker.patch(
        'src.orders.tasks.StockPurchaseOrder.prepare_stock_purchase_order',
    )
    mocker_httpx_post = mocker.patch('src.orders.tasks.httpx.post')
    send_stock_purchase_order_to_reporter({})
    mocker_httpx_post.assert_called_once_with(
        'test_url',
        json=mocker_get_random_accounts_splits_data(),
        headers={'x-api-key': 'test_secret'},
    )
