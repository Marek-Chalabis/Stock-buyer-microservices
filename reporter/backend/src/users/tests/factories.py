import factory

from sqlalchemy.dialects.mssql import MONEY

from users.models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username: str = 'test_username'
    password: str = 'test_password'
    email: str = 'test_email'
    money: MONEY = 10000
