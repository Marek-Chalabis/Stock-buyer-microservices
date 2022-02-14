from sqlalchemy import (
    case,
    desc,
    func,
)
from sqlalchemy.dialects.postgresql import MONEY

from app import db
from trades.enums import (
    DoneBy,
    Operation,
)
from utils.models_mixins import SaveMixin
from utils.typing import QUERY_OR_SUBQUERY


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(length=10), nullable=False)
    name = db.Column(db.String(length=50), nullable=False)
    price = db.Column(
        MONEY,
        nullable=False,
    )
    quantity = db.Column(db.Integer, nullable=False)
    created_date = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    stock_trades = db.relationship('StockTrade', backref='stock', lazy='dynamic')

    @classmethod
    def get_stocks_date_rank_desc(
        cls,
        return_subquery: bool = False,
    ) -> QUERY_OR_SUBQUERY:
        """Ordered stocks by desc creation date.

        date_rank_desc=1 will be most recent
        date_rank_desc=n will be next after recent

        Added fields to Stock:
            - date_rank_desc
        """
        query = db.session.query(
            cls,
            func.rank()
            .over(order_by=desc(cls.created_date), partition_by=cls.symbol)
            .label('date_rank_desc'),
        )
        return query.subquery() if return_subquery else query.all()

    @classmethod
    def get_stocks(cls, return_subquery: bool = False) -> QUERY_OR_SUBQUERY:
        """Stocks grouped by symbol with  basic data.

        Row fields:
            - symbol
            - current_price
            - previous_price
            - available_quantity
        """
        stocks_date_rank_desc = cls.get_stocks_date_rank_desc(return_subquery=True)
        trades_in_user_posses = (
            db.session.query(
                cls.symbol,
                func.sum(
                    case(
                        [
                            (
                                StockTrade.operation == Operation.BUY,
                                StockTrade.quantity,
                            ),
                            (
                                StockTrade.operation == Operation.SELL,
                                -StockTrade.quantity,
                            ),
                        ],
                        else_=0,
                    ),
                ).label('user_trades_quantity'),
            )
            .join(StockTrade, isouter=True)
            .group_by(cls.symbol)
        ).subquery()
        date_rank_price = lambda rank: func.sum(  # noqa: E731
            case(
                [
                    (
                        stocks_date_rank_desc.c.date_rank_desc == rank,
                        stocks_date_rank_desc.c.price,
                    ),
                ],
                else_=None,
            ),
        )
        query = (
            db.session.query(
                stocks_date_rank_desc.c.symbol,
                date_rank_price(1).label('current_price'),
                date_rank_price(2).label('previous_price'),
                (
                    func.sum(stocks_date_rank_desc.c.quantity)
                    - trades_in_user_posses.c.user_trades_quantity
                ).label('available_quantity'),
            )
            .join(
                trades_in_user_posses,
                trades_in_user_posses.c.symbol == stocks_date_rank_desc.c.symbol,
            )
            .group_by(
                stocks_date_rank_desc.c.symbol,
                trades_in_user_posses.c.user_trades_quantity,
            )
            .order_by(stocks_date_rank_desc.c.symbol)
        )
        return query.subquery() if return_subquery else query.all()

    @classmethod
    def get_last_stock_by_symbol(cls, symbol: str) -> 'Stock':
        return (
            db.session.query(cls)
            .filter_by(symbol=symbol)
            .order_by(desc(cls.created_date))
            .first()
        )

    @property
    def available_quantity(self) -> int:
        stocks = self.get_stocks(return_subquery=True)
        return (
            db.session.query(stocks)
            .filter_by(symbol=self.symbol)
            .first()
            .available_quantity
        )


class StockTrade(SaveMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    operation = db.Column(db.Enum(Operation), nullable=False)
    done_by = db.Column(db.Enum(DoneBy), nullable=False)
    created_date = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    user_id = db.Column(db.Integer, db.ForeignKey(column='user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey(column='stock.id'), nullable=False)
