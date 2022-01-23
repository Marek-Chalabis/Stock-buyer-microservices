import httpx

from src.api.schemas import TradeFill
from src.core.config import settings
from src.orders.stock_order import StockPurchaseOrder


async def send_stock_purchase_order_to_reporter(trade_fill: TradeFill) -> None:
    endpoint = settings.reporter_server_client['stocks-purchase-orders']
    stock_purchase_order = StockPurchaseOrder(
        trade_fill=trade_fill,
    ).prepare_stock_purchase_order()
    httpx.post(
        endpoint,
        json=stock_purchase_order,
        headers={'x-api-key': settings.REPORTER_SERVER_KEY_SECRET},
    )
