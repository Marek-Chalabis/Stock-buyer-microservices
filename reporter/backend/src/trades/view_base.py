from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from flask import (
    flash,
    render_template,
    request,
)
from flask.typing import ResponseReturnValue
from flask.views import View
from flask_login import (
    current_user,
    login_required,
)

from trades.enums import (
    DoneBy,
    Operation,
)
from trades.forms import (
    BuyTradesForm,
    SellTradesForm,
)
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
        self._sell_trades_form = SellTradesForm()

    @property
    @abstractmethod
    def template_to_render(self) -> str:
        """Template for view."""

    @property
    @abstractmethod
    def data_for_template(self) -> dict[str:Any]:
        """Data to pass to template."""

    def dispatch_request(self) -> ResponseReturnValue:
        self._form_handlers()
        return render_template(
            template_name_or_list=self.template_to_render,
            buy_trades_form=self._buy_trades_form,
            sell_trades_form=self._sell_trades_form,
            **self.data_for_template,
        )

    def _form_handlers(self) -> None:
        if 'submit_buy_trades' in request.form:
            self._handle_buy_trades_form()
        if 'submit_sell_trades' in request.form:
            self._handle_sell_trades_form()

    def _handle_buy_trades_form(self) -> None:
        if self._buy_trades_form.validate_on_submit():
            user_money = change_to_decimal(current_user.user_profile.money)
            stock_symbol = request.form.get('bought_stock')
            stock = Stock.get_last_stock_by_symbol(symbol=stock_symbol)
            cost = self._buy_trades_form.amount.data * change_to_decimal(stock.price)
            if cost < user_money:
                stock_trade = StockTrade(
                    quantity=self._buy_trades_form.amount.data,
                    operation=Operation.BUY,
                    done_by=DoneBy.USER,
                    user=current_user,
                    stock=stock,
                ).save()
                flash(
                    f'Successfully bought {stock_trade.quantity} '
                    + f'{stock_trade.stock.symbol} trades',
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

    def _handle_sell_trades_form(self) -> None:
        if self._sell_trades_form.validate_on_submit():
            stock_symbol = request.form.get('sold_stock')
            stock = Stock.get_last_stock_by_symbol(symbol=stock_symbol)
            stock_trade = StockTrade(
                quantity=self._buy_trades_form.amount.data,
                operation=Operation.SELL,
                done_by=DoneBy.USER,
                user=current_user,
                stock=stock,
            ).save()
            flash(
                f'Successfully sold {stock_trade.quantity} '
                + f'{stock_trade.stock.symbol} trades',
                category='success',
            )
        else:
            flash_errors_from_form(form=self._sell_trades_form)
