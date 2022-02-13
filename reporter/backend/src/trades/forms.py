import wtforms

from flask import request
from flask_wtf import FlaskForm

from trades.models import Stock


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
