from celery import shared_task
from src import db
from src.api.v1.typing import STOCKS
from src.trades.models import Stock


@shared_task
def add_stock(stocks: STOCKS) -> None:
    stocks = [
        Stock(
            symbol=stock['symbol'],
            name=stock['name'],
            price=stock['price'],
            quantity=stock['quantity'],
        )
        for stock in stocks['stocks']
    ]
    db.session.add_all(stocks)
    db.session.commit()
