import json

from typing import (
    Dict,
    Union,
)

from src.api.schemas import TradeFill
from src.redis import redis

Split = Dict[str, int]
Order = Dict[str, Union[float, Split]]


class StockPurchaseOrder:
    def __init__(self, trade_fill: TradeFill):
        self.trade_fill = trade_fill

    @property
    def accounts_splits(self) -> Dict[str, float]:
        return json.loads(redis.get('accounts_splits'))

    def prepare_stock_purchase_order(self) -> Order:
        return {
            'price': self.trade_fill.price,
            'order': self._get_divided_stock_purchase_order(),
        }

    def _get_divided_stock_purchase_order(self) -> Split:
        """Prepare stock order based on accounts share based on trade fill."""
        split = {
            account: int((percent / 100) * self.trade_fill.quantity)
            for account, percent in self.accounts_splits.items()
        }
        sorted_split = self._sort_split(split=split)
        return self._add_missing_quantity_from_trade_fill(split=sorted_split)

    def _sort_split(self, split: Split) -> Split:
        """Order split by quantity."""
        return {
            account: quantity
            for account, quantity in sorted(
                split.items(),
                key=lambda account_order: account_order[1],
                reverse=True,
            )
        }

    def _add_missing_quantity_from_trade_fill(self, split: Split) -> Split:
        """Add missing quantity from trade fill to order."""
        missing_orders_from_trade_fill = self.trade_fill.quantity - sum(split.values())
        if missing_orders_from_trade_fill:
            ordered_order_keys = list(split.keys())
            for num in range(missing_orders_from_trade_fill):
                split[ordered_order_keys[num]] += 1
        return split
