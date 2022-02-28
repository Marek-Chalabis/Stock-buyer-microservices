from decimal import Decimal

import pytest
import wtforms

from flask_login import login_user

from src.trades.forms import (
    BuyTradesForm,
    SellTradesForm,
)


class TestBuyTradesForm:
    def test_validate_amount(self, mocker, user_in_db, stock):
        mocker.patch(
            'src.trades.forms.Stock.get_last_stock_by_symbol', return_value=stock
        )
        login_user(user_in_db)
        mock_amount = mocker.Mock(data=Decimal(2))
        buy_trades_form = BuyTradesForm()
        with pytest.raises(wtforms.validators.ValidationError):
            buy_trades_form.validate_amount(mock_amount)


class TestSellTradesForm:
    def test_validate_amount(self, mocker, user_in_db, stock):
        mocker.patch('src.trades.forms.request.form.get', return_value=stock.symbol)
        mocker_currently_acquired = [
            mocker.Mock(symbol=stock.symbol, currently_acquired=1),
        ]
        mocker.patch(
            'src.users.models.User.quantity_of_acquired_trades',
            new_callable=mocker.PropertyMock,
            return_value=mocker_currently_acquired,
        )
        login_user(user_in_db)
        mock_amount = mocker.Mock(data=Decimal(2))
        sell_trades_form = SellTradesForm()
        with pytest.raises(wtforms.validators.ValidationError):
            sell_trades_form.validate_amount(mock_amount)
