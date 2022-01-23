from typing import Dict

from fastapi import APIRouter
from pydantic import (
    BaseModel,
    ConstrainedFloat,
    ConstrainedStr,
    Field,
)

router = APIRouter()


class Account(ConstrainedStr):
    min_length = 1
    max_length = 30


class Split(ConstrainedFloat):
    ge = 0
    le = 100


class AccountsSplits(BaseModel):
    __root__: Dict[Account, Split]

    def dict(self, *args, **kwargs) -> Dict[str, float]:  # type: ignore
        """Object in dict form without __root__ key."""
        dict_with_root = super().dict(*args, **kwargs)
        return dict_with_root['__root__']


class TradeFill(BaseModel):
    stock_ticker: str = Field(min_length=1, max_length=30)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
