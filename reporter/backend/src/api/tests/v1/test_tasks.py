from src.api.v1.tasks import add_stock
from src.trades.models import Stock


def test_add_stock(db, stocks):
    add_stock(stocks)
    assert db.session.query(Stock).count() == 2
