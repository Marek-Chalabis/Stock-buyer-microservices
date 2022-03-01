"""register factories and fixtures."""
import pytest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session

from src import create_app
from src import db as _db
from src.api.tests.conftest import *
from src.config import DevelopmentConfig
from src.trades.tests.conftest import *
from src.users.tests.conftest import *


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
        session = db.create_scoped_session(
            options={'bind': connection, 'binds': {}},
        )
        db.session = session
        yield session
        session.remove()
