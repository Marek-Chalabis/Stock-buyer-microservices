# These methods are not tested or optimised, they are just for tests/development
import datetime
import random

from decimal import Decimal
from itertools import chain

import httpx

from src import db
from src.developmnent_utils import development_utils
from src.trades.enums import (
    DoneBy,
    Operation,
)
from src.trades.models import (
    Stock,
    StockTrade,
)
from src.users.models import User
from src.utils.type_parsers import change_to_decimal


def random_date_between(start: datetime, end: datetime) -> datetime:
    return start + datetime.timedelta(
        seconds=random.randint(
            0,
            int(
                (end.replace(tzinfo=None) - start.replace(tzinfo=None)).total_seconds()
            ),
        ),
    )


def restart_db() -> None:
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('DB restarted')


def populate_db_with_random_users() -> None:
    users_to_add = []
    random_users = httpx.get(f'https://randomuser.me/api/?results=35')
    users_data = []
    for random_user in random_users.json()['results']:
        users_to_add.append(
            User(
                username=random_user['login']['username'],
                password=random_user['login']['password'],
                email=random_user['email'],
            )
        )
        users_data.append(
            (random_user['login']['username'], random_user['login']['password'])
        )
    db.session.add_all(users_to_add)
    db.session.commit()
    for user_to_add in users_to_add:
        user_to_add.user_profile.money = Decimal(random.randint(1000, 500000))
        user_to_add.user_profile.trade_bot = random.choice([True, False])
    db.session.commit()
    print('Random users added\n, save this data for develop:')
    for user_data in users_data:
        print(f'User: "{user_data[0]}" Password: "{user_data[1]}"')


def populate_db_with_random_stocks() -> None:
    stocks_to_add = []
    random_stocks = list(
        chain.from_iterable(
            [
                httpx.get(
                    'http://stock_screener:8000/api/v1/stocks?number_of_stocks=500'
                ).json()
                for _ in range(50)
            ]
        )
    )
    for random_stock in random_stocks:
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=1500)
        created_date = random_date_between(start=start, end=end)
        stocks_to_add.append(
            Stock(
                symbol=random_stock['symbol'],
                name=random_stock['name'],
                price=random_stock['price'],
                quantity=random_stock['quantity'],
                created_date=created_date,
            )
        )
    db.session.add_all(stocks_to_add)
    db.session.commit()
    print('Random stocks created')


def populate_db_with_random_stock_trades() -> None:
    stocks = Stock.query.all()
    users = User.query.all()
    for _ in range(15000):
        random_stock = random.choice(stocks)
        next_random_stock = (
            db.session.query(Stock)
            .filter(
                Stock.created_date > random_stock.created_date,
                Stock.symbol == random_stock.symbol,
            )
            .order_by(Stock.created_date.desc())
            .first()
        )
        start_date = random_stock.created_date
        end_date = (
            next_random_stock.created_date
            if next_random_stock
            else datetime.datetime.now()
        )
        created_date = random_date_between(start=start_date, end=end_date)
        random_quantity = None
        random_operation = random.choice([Operation.SELL, Operation.BUY])
        if random_operation == Operation.SELL:
            users_with_stocks = (
                db.session.query(User)
                .join(StockTrade, User.id == StockTrade.user_id)
                .join(Stock, StockTrade.stock_id == Stock.id)
                .filter(
                    StockTrade.stock_id == Stock.id,
                    StockTrade.user_id == User.id,
                    Stock.symbol == random_stock.symbol,
                )
                .all()
            )
            if users_with_stocks:
                random_user = random.choice(users_with_stocks)
                user_stocks_quantity = [
                    x
                    for x in random_user.quantity_of_acquired_trades
                    if x[0] == random_stock.symbol
                ]
                if user_stocks_quantity:
                    max_quantity = user_stocks_quantity[0][1]
                    random_quantity = random.randint(0, max_quantity)
        if random_operation == Operation.BUY:
            random_user = random.choice(users)
            max_quantity_for_user = int(
                change_to_decimal(random_user.user_profile.money)
                / change_to_decimal(random_stock.price)
            )
            random_quantity = random.randint(
                0, min(max_quantity_for_user, random_stock.available_quantity)
            )
        if random_quantity:
            stock_to_add = StockTrade(
                quantity=random_quantity,
                operation=random_operation,
                created_date=created_date,
                done_by=DoneBy.USER,
                user=random_user,
                stock=random_stock,
            )
            db.session.add(stock_to_add)
            db.session.commit()
    print('Random stocks trades created')


@development_utils.cli.command('restart_db')
def _() -> None:
    restart_db()


@development_utils.cli.command('populate_db_with_random_users')
def _() -> None:
    populate_db_with_random_users()


@development_utils.cli.command('populate_db_with_random_stocks')
def _() -> None:
    populate_db_with_random_stocks()


@development_utils.cli.command('populate_db_with_random_stock_trades')
def _() -> None:
    populate_db_with_random_stock_trades()


@development_utils.cli.command('create_new_develop_db_with_random_data')
def create_new_develop_db_with_random_data() -> None:
    restart_db()
    populate_db_with_random_users()
    populate_db_with_random_stocks()
    populate_db_with_random_stock_trades()
    print('DB for development created')
