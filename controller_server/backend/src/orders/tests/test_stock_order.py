from unittest.mock import PropertyMock

import pytest

from src.api.schemas import TradeFill
from src.orders.stock_order import StockPurchaseOrder


class TestStockPurchaseOrder:
    @pytest.fixture
    def stock_purchase_order(self):
        return StockPurchaseOrder(
            trade_fill=TradeFill(
                stock_ticker='test_stock',
                price=100,
                quantity=10,
            ),
        )

    def test_accounts_splits(self, mocker, stock_purchase_order):
        mocker.patch('src.orders.stock_order.redis.get', return_value='{"test": 1}')
        assert stock_purchase_order.accounts_splits == {'test': 1}

    def test_prepare_stock_purchase_order(self, mocker, stock_purchase_order):
        mocker.patch(
            'src.orders.stock_order.StockPurchaseOrder._get_divided_stock_purchase_order',
            return_value='tested_order',
        )
        assert stock_purchase_order.prepare_stock_purchase_order() == {
            'order': 'tested_order',
            'stock_ticker_price': 100.0,
        }

    @pytest.mark.parametrize(
        ('tested_accounts_splits', 'tested_quantity', 'expected_result'),
        [
            ({'test_account_1': 100}, 10, {'test_account_1': 10}),
            (
                {
                    'test_account_1': 34,
                    'test_account_2': 33,
                    'test_account_3': 33,
                },
                10,
                {
                    'test_account_1': 3,
                    'test_account_2': 3,
                    'test_account_3': 3,
                },
            ),
            (
                {
                    'test_account_1': 34,
                    'test_account_2': 33,
                    'test_account_3': 33,
                },
                11,
                {
                    'test_account_1': 3,
                    'test_account_2': 3,
                    'test_account_3': 3,
                },
            ),
            (
                {
                    'test_account_1': 50,
                    'test_account_2': 50,
                },
                1,
                {
                    'test_account_1': 0,
                    'test_account_2': 0,
                },
            ),
            (
                {
                    'test_account_1': 50,
                    'test_account_2': 50,
                },
                2,
                {
                    'test_account_1': 1,
                    'test_account_2': 1,
                },
            ),
        ],
    )
    def test_get_divided_stock_purchase_order_split(
        self,
        mocker,
        tested_accounts_splits,
        tested_quantity,
        expected_result,
    ):
        mocker.patch(
            'src.orders.stock_order.StockPurchaseOrder.accounts_splits',
            new_callable=PropertyMock,
            return_value=tested_accounts_splits,
        )
        mocker_add_missing_quantity_from_trade_fill = mocker.patch(
            'src.orders.stock_order.StockPurchaseOrder._add_missing_quantity_from_trade_fill'
        )
        mocker_sort_split = mocker.patch(
            'src.orders.stock_order.StockPurchaseOrder._sort_split'
        )
        tested_divided_stock_purchase_order = StockPurchaseOrder(
            trade_fill=TradeFill(
                stock_ticker='test_stock',
                price=100,
                quantity=tested_quantity,
            ),
        )._get_divided_stock_purchase_order()
        assert (
            tested_divided_stock_purchase_order
            == mocker_add_missing_quantity_from_trade_fill(split=mocker_sort_split())
        )

    def test_sort_split(self, stock_purchase_order):
        tested_order = stock_purchase_order._sort_split(
            split={
                'test_account_1': 1,
                'test_account_2': 3,
                'test_account_3': 2,
            }
        )
        assert list(tested_order.items()) == [
            ('test_account_2', 3),
            ('test_account_3', 2),
            ('test_account_1', 1),
        ]

    @pytest.mark.parametrize(
        ('tested_quantity', 'tested_split', 'expected_result'),
        [
            (
                9,
                {
                    'test_account_1': 3,
                    'test_account_2': 3,
                    'test_account_3': 3,
                },
                {
                    'test_account_1': 3,
                    'test_account_2': 3,
                    'test_account_3': 3,
                },
            ),
            (
                11,
                {
                    'test_account_1': 3,
                    'test_account_2': 3,
                    'test_account_3': 3,
                },
                {
                    'test_account_1': 4,
                    'test_account_2': 4,
                    'test_account_3': 3,
                },
            ),
        ],
    )
    def test_add_missing_quantity_from_trade_fill(
        self,
        stock_purchase_order,
        tested_quantity,
        tested_split,
        expected_result,
    ):
        stock_purchase_order.trade_fill.quantity = tested_quantity
        assert (
            stock_purchase_order._add_missing_quantity_from_trade_fill(
                split=tested_split
            )
            == expected_result
        )
