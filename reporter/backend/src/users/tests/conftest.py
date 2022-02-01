import pytest

from pytest_factoryboy import register

from users.tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def user_in_db(db, user):
    db.session.add(user)
    db.session.commit()
    return user
