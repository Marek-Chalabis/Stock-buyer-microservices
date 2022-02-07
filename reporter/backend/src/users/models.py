from decimal import Decimal

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import MONEY

from app import (
    bcrypt,
    db,
)


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
        self.password_hash = bcrypt.generate_password_hash(plain_password).decode(
            'utf-8'
        )

    def verify_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username: str, email: str, password: str) -> 'User':
        user_to_create = cls(username=username, email=email, password=password)
        db.session.add(user_to_create)
        db.session.commit()
        return user_to_create


class UserProfile(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    money = db.Column(
        MONEY,
        nullable=False,
        default=0,
    )
    trade_bot = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def money_in_decimal(self) -> Decimal:
        return Decimal(self.money[1:])
