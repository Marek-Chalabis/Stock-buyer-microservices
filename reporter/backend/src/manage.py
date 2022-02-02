# These methods are not tested or optimised, they are just for tests/development
import random

import httpx

from flask.cli import FlaskGroup

from app import db, create_app
from config import FlaskConfig
from users.models import User

app = create_app()
cli = FlaskGroup(app)


def is_development_mode() -> bool:
    if FlaskConfig.FLASK_ENV != 'development':
        print('Command available only in development mode')
        return False
    return True


@cli.command('restart_main_db')
def restart_main_db() -> None:
    if is_development_mode():
        db.drop_all()
        db.create_all()
        db.session.commit()
        print('Main DB restarted')


@cli.command('populate_db_with_random_users')
def populate_db_with_random_users() -> None:
    if is_development_mode():
        number_of_users = 20
        users_to_add = []
        random_users = httpx.get(
            f'https://randomuser.me/api/?results={number_of_users}'
        )
        for random_user in random_users.json()['results']:
            users_to_add.append(
                User(
                    username=random_user['login']['username'],
                    password=random_user['login']['password'],
                    email=random_user['email'],
                    money=random.randint(0, 10000),
                )
            )
        db.session.add_all(users_to_add)
        db.session.commit()
        print(User.query.all())


@cli.command('show_users')
def show_users() -> None:
    print(User.query.all())


if __name__ == "__main__":
    cli()
