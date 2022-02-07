import enum


class Operation(str, enum.Enum):
    SELL = 'sell'
    BUY = 'buy'


class StocksHierarchy(enum.Enum):
    CURRENT = 1
    PREVIOUS = 2


class DoneBy(str, enum.Enum):
    USER = 'user'
    BOT = 'bot'
