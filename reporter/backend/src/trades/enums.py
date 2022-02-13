import enum


class Operation(enum.Enum):
    SELL = 'sell'
    BUY = 'buy'


class DoneBy(enum.Enum):
    USER = 'user'
    BOT = 'bot'
