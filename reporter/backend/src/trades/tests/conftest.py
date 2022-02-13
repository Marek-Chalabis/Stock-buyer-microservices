import pytest

from pytest_factoryboy import register

from trades.tests.factories import (
    StockFactory,
    StockTradeFactory,
)

register(StockFactory)
register(StockTradeFactory)


@pytest.fixture
def stock_in_db(db, stock):
    db.session.add(stock)
    db.session.commit()
    return stock
