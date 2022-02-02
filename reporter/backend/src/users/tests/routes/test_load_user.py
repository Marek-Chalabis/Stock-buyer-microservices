from users.routes import load_user


def test_load_user_user_exists(db, user):
    db.session.add(user)
    assert load_user('1') == user


def test_load_user_user_not_exists():
    assert not load_user('1')
