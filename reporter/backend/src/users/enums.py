import enum


class MoneyOperation(str, enum.Enum):
    DEPOSIT = 'Deposit'
    PAY_OUT = 'Pay out'
