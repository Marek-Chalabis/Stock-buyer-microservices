from typing import Dict

from fastapi import (
    APIRouter,
    BackgroundTasks,
    status,
)

from src.api.schemas import TradeFill
from src.core.logger import logger
from src.orders.tasks import send_stock_purchase_order_to_reporter

router = APIRouter()


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def trade_fills(
    trade_fill: TradeFill,
    background_tasks: BackgroundTasks,
) -> Dict[str, str]:
    """Trigger task that will process trade fill and sends it to a reporter."""
    background_tasks.add_task(send_stock_purchase_order_to_reporter, trade_fill)
    logger.info('Received trade fill: {0}'.format(trade_fill))
    return {'message': 'Trade fill accepted'}
