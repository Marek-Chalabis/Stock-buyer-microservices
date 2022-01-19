from typing import Dict

from fastapi import APIRouter
from pydantic import BaseModel, confloat, constr
from pydantic import Field

router = APIRouter()

Account = constr(min_length=1, max_length=30)
Split = confloat(ge=0, le=100)


class AccountsSplits(BaseModel):
    __root__: Dict[Account, Split]

    def dict(self) -> Dict[str, float]:
        """Returns object in dict form without __root__ key."""
        dict_with_root = super().dict()
        return dict_with_root['__root__']


class TradeFill(BaseModel):
    stock_name: str = Field(min_length=1, max_length=30)
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
