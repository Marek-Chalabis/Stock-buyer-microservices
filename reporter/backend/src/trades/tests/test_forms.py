from decimal import Decimal

import pytest
import wtforms

from flask_login import login_user

from trades.forms import BuyTradesForm


class TestBuyTradesForm:
    def test_validate_amount(self, mocker, user_in_db):
        login_user(user_in_db)
        mock_amount = mocker.Mock(data=Decimal(11))
        buy_trades_form = BuyTradesForm()
        with pytest.raises(wtforms.validators.ValidationError):
            buy_trades_form.validate_amount(mock_amount)
