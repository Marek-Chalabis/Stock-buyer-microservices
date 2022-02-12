from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

import flask_login

from flask import (
    flash,
    render_template,
    request,
)
from flask.typing import ResponseReturnValue
from flask.views import View
from flask_login import login_required

from trades.enums import (
    DoneBy,
    Operation,
)
from trades.forms import BuyTradesForm
from trades.models import (
    Stock,
    StockTrade,
)
from utils.type_parsers import change_to_decimal
from utils.view_utils import flash_errors_from_form


class BaseSellBuyTradeView(ABC, View):
    """Base class providing methods to handle buy/sell action on trades.

    Forms are connected by id: bought_stock, TODO
    """

    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self) -> None:
        self._buy_trades_form = BuyTradesForm()

    @property
    @abstractmethod
    def template_to_render(self) -> str:
        """Template for view."""

    @property
    @abstractmethod
    def data_for_template(self) -> dict[str:Any]:
        """Data to pass to template."""

    def dispatch_request(self) -> ResponseReturnValue:
        self._handle_buy_trades_form()
        return render_template(
            template_name_or_list=self.template_to_render,
            buy_trades_form=self._buy_trades_form,
            **self.data_for_template,
        )

    def _handle_buy_trades_form(self) -> None:  # TODO extract to more methods
        if self._buy_trades_form.validate_on_submit():
            user_money = change_to_decimal(
                flask_login.current_user.user_profile.money,
            )
            stock_symbol = request.form.get('bought_stock')
            stock = Stock.get_last_stock_by_symbol(symbol=stock_symbol)
            stock_price = change_to_decimal(stock.price)
            cost = self._buy_trades_form.amount.data * stock_price
            if cost < user_money:
                stock_trade = StockTrade(
                    quantity=self._buy_trades_form.amount.data,
                    operation=Operation.BUY,
                    done_by=DoneBy.USER,
                    user=flask_login.current_user,
                    stock=stock,
                ).save()
                plural_trades = 'trade' + 's' if stock_trade.quantity > 1 else ''
                flash(
                    f'Successfully bought {stock_trade.quantity} '
                    + f'{stock_trade.stock.symbol} {plural_trades}',
                    category='success',
                )
            else:
                flash(
                    f'You do not have enough money({user_money}$) '
                    + f'for this purchase({cost}$)',
                    category='danger',
                )
        else:
            flash_errors_from_form(form=self._buy_trades_form)
