import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session

from app import create_app
from app import db as _db
from config import FlaskConfigTesting
# register factories and fixtures
from trades.tests.conftest import *
from users.tests.conftest import *


@pytest.fixture
def app() -> Flask:
    app = create_app(config=FlaskConfigTesting)
    yield app


@pytest.fixture
def db(app) -> SQLAlchemy:
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db) -> scoped_session:
    connection = db.engine.connect()
    transaction = connection.begin()

    options = {'bind': connection, 'binds': {}}
    session_ = db.create_scoped_session(options=options)  # noqa: WPS120

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
