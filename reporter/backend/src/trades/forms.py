import wtforms

from flask import request
from flask_login import current_user
from flask_wtf import FlaskForm

from src.trades.models import Stock


class BuyTradesForm(FlaskForm):
    amount = wtforms.DecimalField(
        label='Amount:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.NumberRange(min=1),
        ],
    )
    submit_buy_trades = wtforms.SubmitField(label='Buy trades')

    def validate_amount(self, amount_to_validate: wtforms.DecimalField) -> None:
        stock_symbol = request.form.get('bought_stock')
        available_quantity = Stock.get_last_stock_by_symbol(
            symbol=stock_symbol,
        ).quantity
        if amount_to_validate.data > available_quantity:
            raise wtforms.ValidationError(
                f'You are trying to buy more stocks("{stock_symbol}") '
                + f'then are available({available_quantity})',
            )


class SellTradesForm(FlaskForm):
    amount = wtforms.DecimalField(
        label='Amount:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.NumberRange(min=1),
        ],
    )
    submit_sell_trades = wtforms.SubmitField(label='Sell trades')

    def validate_amount(self, amount_to_validate: wtforms.DecimalField) -> None:
        stock_symbol = request.form.get('sold_stock')
        available_quantity = next(
            stock
            for stock in current_user.quantity_of_acquired_trades
            if stock.symbol == stock_symbol
        ).currently_acquired
        if amount_to_validate.data > available_quantity:
            raise wtforms.ValidationError(
                f'You are trying to sell more stocks("{stock_symbol}") '
                + f'then you have({available_quantity})',
            )
