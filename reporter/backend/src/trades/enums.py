import enum


class Operation(str, enum.Enum):
    SELL = 'sell'
    BUY = 'buy'


class DoneBy(str, enum.Enum):
    USER = 'user'
    BOT = 'bot'
