import pytest

from flask import Flask

from app import create_app
from app import db as _db
from config import FlaskConfigTesting


@pytest.fixture
def app() -> Flask:
    app = create_app(config=FlaskConfigTesting)
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def app_client(app):
    return app.test_client()


@pytest.fixture
def app_client_class(request, app_client):
    if request.cls is not None:
        request.cls.app_client = app_client


@pytest.fixture
def app_client_endpoint(app):
    return app.test_client()


@pytest.fixture
def db(app):
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
