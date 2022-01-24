from fastapi import status
from fastapi.testclient import TestClient

from src.api.api_v1.api import authorizer
from src.main import app
from src.orders.tasks import send_stock_purchase_order_to_reporter

client = TestClient(app)

app.dependency_overrides[authorizer] = lambda: None


def test_trade_fills(mocker):
    mocker_add_task = mocker.patch(
        'src.api.api_v1.endpoints.fills.BackgroundTasks.add_task',
    )
    tested_trade_fill = {
        'stock_ticker': 'test',
        'price': 1,
        'quantity': 2,
    }
    response = client.post('/api/v1/trade-fills/', json=tested_trade_fill)
    assert response.status_code == status.HTTP_202_ACCEPTED
    mocker_add_task.assert_called_once_with(
        send_stock_purchase_order_to_reporter,
        tested_trade_fill,
    )
