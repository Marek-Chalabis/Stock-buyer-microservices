from fastapi import (
    APIRouter,
    status,
)

from src.api.schemas import AccountsSplits
from src.redis import redis

router = APIRouter()


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def splits_accounts(
    accounts_split_data: AccountsSplits,
) -> None:
    """Set Accounts trade split."""
    redis.hmset('accounts_split_data', accounts_split_data.dict())
