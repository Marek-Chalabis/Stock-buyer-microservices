import random

from dataclasses import (
    asdict,
    dataclass,
)
from typing import (
    Any,
    Dict,
    List,
)

from src.stocks.constants import STOCK_TICKER


@dataclass
class Stock:
    symbol: str
    name: str
    price: float
    quantity: int


def generate_random_stocks(number_of_stocks: int) -> List[Dict[str, Any]]:
    stocks_tickers = random.sample(STOCK_TICKER, number_of_stocks)
    return [
        asdict(
            Stock(
                symbol=stock_ticker[0],
                name=stock_ticker[1],
                price=round(random.uniform(10, 1000), 2),  # noqa: S311
                quantity=random.randint(1, 200),  # noqa: S311
            ),
        )
        for stock_ticker in stocks_tickers
    ]
