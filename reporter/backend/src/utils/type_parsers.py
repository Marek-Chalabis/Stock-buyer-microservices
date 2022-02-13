from decimal import Decimal
from functools import singledispatch
from typing import Any


@singledispatch
def change_to_decimal(value_to_change: Any) -> Decimal:
    return Decimal(value_to_change)


@change_to_decimal.register(str)
def _(value_to_change: str) -> Decimal:
    return Decimal(value_to_change.replace('$', '').replace(',', ''))
