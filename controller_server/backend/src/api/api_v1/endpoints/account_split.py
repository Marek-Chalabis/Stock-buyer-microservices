from typing import Dict

from fastapi import (
    APIRouter,
    status,
)

from src.api.schemas import AccountsSplits
from src.core.logger import logger
from src.redis import redis

router = APIRouter()


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def splits_accounts(
    accounts_splits: AccountsSplits,
) -> Dict[str, str]:
    """Set Accounts trade split."""
    redis.set('accounts_splits', accounts_splits.json())
    logger.info('Received account split: {0}'.format(accounts_splits))
    return {'message': 'Split account accepted'}
