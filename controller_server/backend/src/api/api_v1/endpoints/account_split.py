from fastapi import APIRouter, status
from src.custom_types import AccountsSplitData
from src.redis import r
from src.validators import validate_accounts_split

router = APIRouter()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def splits_accounts(
        accounts_split_data: AccountsSplitData,
) -> None:
    """Saves Accounts trade split."""
    validate_accounts_split(accounts_split_data=accounts_split_data)
    r.hmset('accounts_split_data', accounts_split_data)
