from fastapi import APIRouter, status
from src.redis import r

from src.schemas import AccountsSplits

router = APIRouter()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def splits_accounts(
        accounts_split_data: AccountsSplits,
) -> None:
    """Saves Accounts trade split."""
    r.hmset('accounts_split_data', accounts_split_data.dict())
