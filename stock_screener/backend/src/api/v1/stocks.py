from typing import (
    Any,
    List,
)

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    status,
)

from src import schemas
from src.core.config import settings
from src.stocks.stock import generate_random_stocks

router = APIRouter()


@router.get('', response_model=List[schemas.StockBase])
async def stocks(
    number_of_stocks: int = Query(default=50, ge=1, le=500),
) -> Any:
    if settings.APP_STATUS != 'development':
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Endpoint available only on development.',
        )
    return generate_random_stocks(number_of_stocks=number_of_stocks)
