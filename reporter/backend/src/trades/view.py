from flask import render_template
from flask.typing import ResponseReturnValue
from flask.views import View
from flask_login import login_required
from sqlalchemy import (
    Numeric,
    cast,
)

from app import db
from trades.enums import StocksHierarchy
from trades.models import Stock


class TradesView(View):
    methods = ['GET']
    decorators = [login_required]

    def get_stocks(self):  # TODO typing
        """Stocks with price difference and available quantity to buy."""
        current_stocks_subquery = Stock.get_stocks(return_subquery=True)
        previous_stocks_subquery = Stock.get_stocks(
            stocks_hierarchy=StocksHierarchy.PREVIOUS,
            return_subquery=True,
        )
        available_stocks_subquery = Stock.get_quantity_of_available_stocks_to_buy(
            return_subquery=True,
        )
        return (
            db.session.query(
                current_stocks_subquery,
                available_stocks_subquery.c.available_quantity,
                (
                    current_stocks_subquery.c.price - previous_stocks_subquery.c.price
                ).label('plain_difference'),
                (
                    cast(
                        (
                            (
                                current_stocks_subquery.c.price
                                - previous_stocks_subquery.c.price
                            )
                            * 100
                        )
                        / previous_stocks_subquery.c.price,
                        Numeric(10, 2),
                    )
                ).label('percent_difference'),
            )
            .join(
                previous_stocks_subquery,
                current_stocks_subquery.c.symbol == previous_stocks_subquery.c.symbol,
                isouter=True,
            )
            .join(
                available_stocks_subquery,
                current_stocks_subquery.c.symbol == available_stocks_subquery.c.symbol,
            )
            .order_by(current_stocks_subquery.c.symbol)
            .all()
        )

    def dispatch_request(self) -> ResponseReturnValue:
        return render_template(
            template_name_or_list='stocks.html',
            stocks=self.get_stocks(),
        )
