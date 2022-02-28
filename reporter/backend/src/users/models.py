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

from src import (
    bcrypt,
    db,
)
from src.trades.enums import Operation
from src.trades.models import (
    Stock,
    StockTrade,
)
from src.utils.models_mixins import SaveMixin
from src.utils.type_parsers import change_to_decimal


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

    @property
    def quantity_of_acquired_trades(self) -> List[Row]:
        currently_acquired = func.sum(
            case(
                [(StockTrade.operation == Operation.BUY, StockTrade.quantity)],
                else_=-StockTrade.quantity,
            ),
        )
        return (
            db.session.query(  # noqa: WPS221
                Stock.symbol,
                currently_acquired.label('currently_acquired'),
            )
            .join(Stock.stock_trades)
            .filter(StockTrade.user_id == self.id)
            .group_by(Stock.symbol)
            .having(currently_acquired > 0)
            .order_by(Stock.symbol)
            .all()
        )

    def verify_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)


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
        commit: bool = False,
    ) -> None:
        self.money = change_to_decimal(self.money) + change_to_decimal(  # noqa: WPS601
            amount,
        )
        if commit:
            db.session.commit()
