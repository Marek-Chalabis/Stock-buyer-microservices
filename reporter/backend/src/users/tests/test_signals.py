def test_add_profile_to_user(user_in_db):
    assert user_in_db.user_profile
    assert user_in_db.user_profile.user == user_in_db
