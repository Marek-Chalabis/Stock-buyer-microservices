from fastapi import (
    APIRouter,
    status,
)

from src.api.schemas import TradeFill

router = APIRouter()


@router.post('/', status_code=status.HTTP_202_ACCEPTED) # TODO test this
async def trade_fills(
    trade_fill: TradeFill,
) -> None:
    """Set Accounts trade split."""
    print(trade_fill)
