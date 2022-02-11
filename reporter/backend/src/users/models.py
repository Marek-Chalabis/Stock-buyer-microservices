from decimal import Decimal
from typing import (
    List,
    Union,
)

from flask_login import UserMixin
from sqlalchemy import (
    case,
    func,
)
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.engine import Row

from app import (
    bcrypt,
    db,
)
from trades.enums import Operation
from trades.models import (
    Stock,
    StockTrade,
)
from utils.models_mixins import SaveMixin
from utils.type_parsers import change_to_decimal


class User(SaveMixin, UserMixin, db.Model):
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

    def get_quantity_of_acquired_trades(self) -> List[Row]:
        return (
            db.session.query(
                Stock.symbol,
                func.sum(
                    case(
                        [(StockTrade.operation == Operation.BUY, StockTrade.quantity)],
                        else_=-StockTrade.quantity,
                    )
                ).label('currently_acquired'),
            )
            .join(StockTrade, StockTrade.stock_id == Stock.id)
            .filter(StockTrade.user_id == self.id)
            .group_by(Stock.symbol)
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

    def update_money_by_amount(
        self,
        amount: Union[str, Decimal, float],
        commit: False,
    ) -> None:
        self.money = change_to_decimal(self.money) + change_to_decimal(amount)
        if commit:
            db.session.commit()
