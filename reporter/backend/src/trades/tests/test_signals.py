from decimal import Decimal

import pytest

from trades.enums import Operation
from trades.tests.factories import StockTradeFactory


@pytest.mark.parametrize(
    (
        'tested_operation',
        'expected_result',
    ),
    [
        (Operation.SELL, Decimal(100)),
        (Operation.BUY, Decimal(-100)),
    ],
)
def test_update_user_money_stock_trade(user_in_db, tested_operation, expected_result):
    StockTradeFactory(operation=tested_operation, user=user_in_db)
    assert user_in_db.user_profile.money == expected_result
