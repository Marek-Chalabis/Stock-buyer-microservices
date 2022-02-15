from decimal import Decimal

import pytest

from flask_login import (
    login_required,
    login_user,
)

from app import db
from trades.enums import (
    DoneBy,
    Operation,
)
from trades.forms import BuyTradesForm
from trades.models import StockTrade
from trades.view_base import BaseSellBuyTradeView


class BaseSellBuyTradeViewConcrete(BaseSellBuyTradeView):
    template_to_render = 'test_template'
    data_for_template = {'test_key': 'test_data'}


class TestBaseSellBuyTradeView:
    @pytest.fixture
    def buy_trades_form(self, mocker):
        mocker_buy_trades_form = mocker.patch('trades.view_base.BuyTradesForm')
        mocker_form = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=True),
            amount=mocker.Mock(data=Decimal(1)),
        )
        mocker_buy_trades_form.return_value = mocker_form
        return mocker_buy_trades_form

    @pytest.fixture
    def sell_trades_form(self, mocker):
        mocker_sell_trades_form = mocker.patch('trades.view_base.SellTradesForm')
        mocker_form = mocker.Mock(
            validate_on_submit=mocker.Mock(return_value=True),
            amount=mocker.Mock(data=Decimal(1)),
        )
        mocker_sell_trades_form.return_value = mocker_form
        return mocker_sell_trades_form

    @pytest.fixture
    def class_obj(self, buy_trades_form, sell_trades_form):
        class_obj = BaseSellBuyTradeViewConcrete()
        class_obj._buy_trades_form = buy_trades_form
        class_obj._sell_trades_form = sell_trades_form
        return BaseSellBuyTradeViewConcrete()

    def test_methods(self, class_obj):
        assert class_obj.methods == ['GET', 'POST']

    def test_decorators(self, class_obj):
        assert class_obj.decorators == [login_required]

    def test_init(self):
        class_obj = BaseSellBuyTradeViewConcrete()
        assert isinstance(class_obj._buy_trades_form, BuyTradesForm)

    def test_template_to_render(self, class_obj):
        assert class_obj.template_to_render == 'test_template'

    def test_data_for_template(self, class_obj):
        assert class_obj.data_for_template == {'test_key': 'test_data'}

    def test_dispatch_request_form_handlers(self, mocker, class_obj):
        mocker.patch('trades.view_base.render_template')
        mocker_form_handlers = mocker.patch(
            'trades.view_base.BaseSellBuyTradeView._form_handlers',
        )
        class_obj.dispatch_request()
        mocker_form_handlers.assert_called_once_with()

    def test_dispatch_request_render_template(self, mocker, class_obj):
        mocker_render_template = mocker.patch('trades.view_base.render_template')
        mocker.patch('trades.view_base.BaseSellBuyTradeView._form_handlers')
        assert class_obj.dispatch_request() == mocker_render_template()
        class_obj.dispatch_request()
        mocker_render_template.assert_called_with(
            template_name_or_list='test_template',
            buy_trades_form=class_obj._buy_trades_form,
            sell_trades_form=class_obj._sell_trades_form,
            test_key='test_data',
        )

    @pytest.mark.parametrize(
        (
            'tested_form',
            'expected_method_call',
        ),
        [
            ({'submit_buy_trades': None}, '_handle_buy_trades_form'),
            ({'submit_sell_trades': None}, '_handle_sell_trades_form'),
        ],
    )
    def test_form_handlers(
        self,
        mocker,
        class_obj,
        app,
        tested_form,
        expected_method_call,
    ):
        with app.test_request_context():
            mocker_request = mocker.patch('trades.view_base.request')
            mocker_request.form = tested_form
            mocker_expected_method = mocker.patch(
                f'trades.view_base.BaseSellBuyTradeView.{expected_method_call}',
            )
            class_obj._form_handlers()
            mocker_expected_method.assert_called_once_with()

    def test_handle_buy_trades_form_invalid_form(
        self,
        mocker,
        class_obj,
        buy_trades_form,
        user_in_db,
    ):
        mocker_flash_errors_from_form = mocker.patch(
            'trades.view_base.flash_errors_from_form',
        )
        class_obj._buy_trades_form.validate_on_submit = mocker.Mock(return_value=False)
        class_obj._handle_buy_trades_form()
        mocker_flash_errors_from_form.assert_called_once_with(
            form=class_obj._buy_trades_form,
        )

    def test_handle_buy_trades_form_missing_money(
        self,
        mocker,
        class_obj,
        buy_trades_form,
        user_in_db,
        stock_in_db,
    ):
        mocker_flash = mocker.patch('trades.view_base.flash')
        mocker.patch('trades.view_base.request.form.get', return_value='TEST')
        login_user(user_in_db)
        class_obj._handle_buy_trades_form()
        mocker_flash.assert_called_once()

    def test_handle_buy_trades_form_stock_trade(
        self,
        mocker,
        class_obj,
        buy_trades_form,
        user_in_db,
        stock_in_db,
    ):
        mocker.patch('trades.view_base.request.form.get', return_value='TEST')
        user_in_db.user_profile.money = Decimal(1000)
        login_user(user_in_db)
        class_obj._handle_buy_trades_form()
        tested_stock_trade = db.session.query(StockTrade).first()
        assert tested_stock_trade
        assert tested_stock_trade.done_by == DoneBy.USER
        assert tested_stock_trade.operation == Operation.BUY

    def test_handle_buy_trades_form_flash(
        self,
        mocker,
        class_obj,
        buy_trades_form,
        user_in_db,
        stock_in_db,
    ):
        mocker_flash = mocker.patch('trades.view_base.flash')
        mocker.patch('trades.view_base.request.form.get', return_value='TEST')
        user_in_db.user_profile.money = Decimal(1000)
        login_user(user_in_db)
        class_obj._handle_buy_trades_form()
        mocker_flash.assert_called_once()

    def test_handle_sell_trades_form_invalid_form(
        self,
        mocker,
        class_obj,
        buy_trades_form,
        user_in_db,
    ):
        mocker_flash_errors_from_form = mocker.patch(
            'trades.view_base.flash_errors_from_form',
        )
        class_obj._sell_trades_form.validate_on_submit = mocker.Mock(return_value=False)
        class_obj._handle_sell_trades_form()
        mocker_flash_errors_from_form.assert_called_once_with(
            form=class_obj._sell_trades_form,
        )

    def test_handle_sell_trades_form_stock_trade(
        self,
        mocker,
        class_obj,
        buy_trades_form,
        user_in_db,
        stock_in_db,
    ):
        mocker.patch('trades.view_base.request.form.get', return_value='TEST')
        login_user(user_in_db)
        class_obj._handle_sell_trades_form()
        tested_stock_trade = db.session.query(StockTrade).first()
        assert tested_stock_trade
        assert tested_stock_trade.done_by == DoneBy.USER
        assert tested_stock_trade.operation == Operation.SELL

    def test_handle_sell_trades_form_flash(
        self,
        mocker,
        class_obj,
        buy_trades_form,
        user_in_db,
        stock_in_db,
    ):
        mocker_flash = mocker.patch('trades.view_base.flash')
        mocker.patch('trades.view_base.request.form.get', return_value='TEST')
        login_user(user_in_db)
        class_obj._handle_sell_trades_form()
        mocker_flash.assert_called_once()
