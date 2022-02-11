from sqlalchemy import event

from trades.enums import Operation
from trades.models import StockTrade
from utils.type_parsers import change_to_decimal


@event.listens_for(target=StockTrade, identifier='init')
def update_user_money_stock_trade(mapper, connection, stock_trade) -> None:
    amount = stock_trade['quantity'] * change_to_decimal(stock_trade['stock'].price)
    stock_trade['user'].user_profile.update_money_by_amount(
        amount=amount if stock_trade['operation'] == Operation.SELL else -amount,
    )
