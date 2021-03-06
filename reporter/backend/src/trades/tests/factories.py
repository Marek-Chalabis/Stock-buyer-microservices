from datetime import datetime

import factory

from src.trades.enums import (
    DoneBy,
    Operation,
)
from src.trades.models import (
    Stock,
    StockTrade,
)
from src.users.models import User
from src.users.tests.factories import UserFactory


class StockFactory(factory.Factory):
    class Meta:
        model = Stock

    id: int = 1
    symbol: str = 'TEST'
    name: str = 'test_name'
    price: str = '$100'
    quantity: int = 1
    created_date: datetime = datetime.now()


class StockTradeFactory(factory.Factory):
    class Meta:
        model = StockTrade

    id: int = 1
    quantity: int = 1
    operation: Operation = Operation.BUY
    done_by: DoneBy = DoneBy.USER
    created_date: datetime = datetime.now()
    stock: StockFactory = factory.SubFactory(StockFactory)
    user: User = factory.SubFactory(UserFactory)
