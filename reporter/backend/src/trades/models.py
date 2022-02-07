import sqlalchemy

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import MONEY

from app import db
from trades.enums import (
    DoneBy,
    Operation,
    StocksHierarchy,
)


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
        server_default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    stock_trades = db.relationship('StockTrade', backref='stock', lazy='dynamic')

    @classmethod
    def get_stocks(
        cls,
        stocks_hierarchy: StocksHierarchy = StocksHierarchy.CURRENT,
        return_subquery=False,
    ):  # TODO typing
        """Stocks grouped by symbol and by creation date."""
        subquery = db.session.query(
            cls,
            func.rank()
            .over(order_by=Stock.created_date.desc(), partition_by=cls.symbol)
            .label('date_rank_desc'),
        ).subquery()
        query = db.session.query(subquery).filter(
            subquery.c.date_rank_desc == stocks_hierarchy.value
        )
        return query.subquery() if return_subquery else query.all()

    @classmethod
    def get_quantity_of_bought_stocks(cls, return_subquery=False):  # TODO typing
        """Quantity of stocks in possess of the users."""
        query = (
            db.session.query(
                cls.symbol, func.sum(StockTrade.quantity).label('bought_stocks')
            )
            .join(StockTrade, cls.id == StockTrade.stock_id, isouter=True)
            .filter(StockTrade.operation == Operation.BUY.value)
            .group_by(cls.symbol)
        )
        return query.subquery() if return_subquery else query.all()

    @classmethod
    def get_quantity_of_all_stocks(cls, return_subquery=False):  # TODO typing
        """Quantity of all stocks that was added to buy."""
        query = db.session.query(
            cls.symbol, func.sum(cls.quantity).label('all_stocks')
        ).group_by(cls.symbol)
        return query.subquery() if return_subquery else query.all()

    @classmethod
    def get_quantity_of_available_stocks_to_buy(
        cls,
        return_subquery=False,
    ):  # TODO typing
        """Available stocks quantity to buy."""
        bought_stocks = cls.get_quantity_of_bought_stocks(return_subquery=True)
        all_stocks = cls.get_quantity_of_all_stocks(return_subquery=True)
        query = (
            db.session.query(
                bought_stocks.c.symbol,
                (
                    func.sum(all_stocks.c.all_stocks)
                    - func.sum(bought_stocks.c.bought_stocks)
                ).label('available_quantity'),
            )
            .join(
                all_stocks,
                all_stocks.c.symbol == bought_stocks.c.symbol,
                isouter=True,
            )
            .group_by(bought_stocks.c.symbol)
        )
        return query.subquery() if return_subquery else query.all()


class StockTrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    operation = db.Column(db.Enum(Operation), nullable=False)
    done_by = db.Column(db.Enum(DoneBy), nullable=False)
    created_date = db.Column(
        db.DateTime(timezone=True),
        server_default=sqlalchemy.sql.func.now(),
        nullable=False,
    )
    user_id = db.Column(db.Integer, db.ForeignKey(column='user.id'), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey(column='stock.id'), nullable=False)
