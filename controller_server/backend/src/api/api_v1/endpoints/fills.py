from typing import Dict

from fastapi import (
    APIRouter,
    BackgroundTasks,
    status,
)

from src.api.schemas import TradeFill
from src.orders.tasks import send_stock_purchase_order_to_reporter

router = APIRouter()


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def trade_fills(
    trade_fill: TradeFill,
    background_tasks: BackgroundTasks,
) -> Dict[str, str]:
    background_tasks.add_task(send_stock_purchase_order_to_reporter, trade_fill)
    return {'message': 'Trade fill accepted'}
