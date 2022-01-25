import random

from typing import (
    Dict,
    Union,
)

from src.constants import (
    MAX_TRADE_TICKER_PRICE,
    MAX_TRADE_TICKER_QUANTITY,
    MIN_TRADE_TICKER_PRICE,
    MIN_TRADE_TICKER_QUANTITY,
    STOCK_TICKERS,
)

TRADE_FILL = Dict[str, Union[str, float]]


def get_random_fill() -> TRADE_FILL:
    """Random trade fill with random quantity and price."""
    random_trade_ticker = random.choice(STOCK_TICKERS)  # noqa: S311
    random_quantity = random.randint(  # noqa: S311
        MIN_TRADE_TICKER_QUANTITY,
        MAX_TRADE_TICKER_QUANTITY,
    )
    random_price = round(
        random.uniform(MIN_TRADE_TICKER_PRICE, MAX_TRADE_TICKER_PRICE),  # noqa: S311
        2,
    )
    return {
        'stock_ticker': random_trade_ticker,
        'price': random_price,
        'quantity': random_quantity,
    }
