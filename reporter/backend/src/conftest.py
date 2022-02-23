import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session

from app import create_app
from app import db as _db
from config import DevelopmentConfig
# register factories and fixtures
from trades.tests.conftest import *
from users.tests.conftest import *


@pytest.fixture
def app() -> Flask:
    app = create_app(config=DevelopmentConfig)
    yield app


@pytest.fixture
def db(app) -> SQLAlchemy:
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db) -> scoped_session:
    with db.engine.connect() as connection:
        session_ = db.create_scoped_session(options={'bind': connection, 'binds': {}})  # noqa: WPS120
        db.session = session_
        yield session_
        session_.remove()
