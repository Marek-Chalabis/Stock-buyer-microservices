from typing import Any

import flask_login

from sqlalchemy import (
    Numeric,
    cast,
)

from app import db
from trades.models import Stock
from trades.view_base import BaseSellBuyTradeView


class TradesView(BaseSellBuyTradeView):
    template_to_render = 'stocks.html'

    @property
    def data_for_template(self) -> dict[str:Any]:
        stocks = Stock.get_stocks(return_subquery=True)
        trades_for_view = db.session.query(
            stocks,
            (stocks.c.current_price - stocks.c.previous_price).label(
                'plain_difference'
            ),
            (
                cast(
                    ((stocks.c.current_price - stocks.c.previous_price) * 100)
                    / stocks.c.current_price,
                    Numeric(10, 2),
                )
            ).label('percent_difference'),
        ).all()
        return {
            'trades': trades_for_view,
            'user_trades': flask_login.current_user.get_quantity_of_acquired_trades(),
        }
