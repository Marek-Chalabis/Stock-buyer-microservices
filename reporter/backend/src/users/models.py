from decimal import Decimal

from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import MONEY

from app import (
    bcrypt,
    db,
)
from trades.enums import Operation
from trades.models import (
    Stock,
    StockTrade,
)
from users.enums import MoneyOperation


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    email = db.Column(db.String(length=60), nullable=False, unique=True)

    user_profile = db.relationship('UserProfile', backref='user', uselist=False)
    stock_trades = db.relationship('StockTrade', backref='user', lazy='dynamic')

    @property
    def password(self) -> str:
        return self.password

    @password.setter
    def password(self, plain_password) -> None:
        self.password_hash = bcrypt.generate_password_hash(  # noqa: WPS601
            plain_password,
        ).decode(
            'utf-8',
        )

    def verify_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username: str, email: str, password: str) -> 'User':
        user_to_create = cls(username=username, email=email, password=password)
        db.session.add(user_to_create)
        db.session.commit()
        return user_to_create

    def get_quantity_of_acquired_trades(self):  # TODO typing/tests
        bought = (
            db.session.query(
                Stock.symbol,
                func.sum(StockTrade.quantity).label('bought'),
            )
            .join(StockTrade, StockTrade.stock_id == Stock.id)
            .filter(
                StockTrade.user_id == self.id,
                StockTrade.operation == Operation.BUY,
            )
            .group_by(Stock.symbol)
            .subquery()
        )
        sold = (
            db.session.query(
                Stock.symbol,
                func.sum(StockTrade.quantity).label('sold'),
            )
            .join(StockTrade, StockTrade.stock_id == Stock.id)
            .filter(
                StockTrade.user_id == self.id,
                StockTrade.operation == Operation.SELL,
            )
            .group_by(Stock.symbol)
            .subquery()
        )
        return (
            db.session.query(
                bought.c.symbol,
                bought.c.bought,
                sold.c.sold,
                (bought.c.bought - sold.c.sold).label('currently_acquired'),
            )
            .join(sold, sold.c.symbol == bought.c.symbol)
            .order_by(bought.c.symbol)
            .all()
        )


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    money = db.Column(
        MONEY,
        nullable=False,
        default=0,
    )
    trade_bot = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def money_in_decimal(self) -> Decimal:
        return Decimal(self.money[1:].replace(',', ''))

    def change_money_based_on_operation(
        self,
        amount: Decimal,
        operation: MoneyOperation,
    ) -> None:
        operator_for_money_change = (
            '-' if operation == MoneyOperation.PAY_OUT.value else ''
        )
        change_amount = Decimal(f'{operator_for_money_change}{amount}')
        self.money = self.money_in_decimal + change_amount  # noqa: WPS601
        db.session.commit()
