from sqlalchemy import event

from app import db
from users.models import (
    User,
    UserProfile,
)


@event.listens_for(target=User, identifier='after_insert')
def add_profile_to_user(mapper, connection, user) -> None:
    user_profile = UserProfile(user=user)
    db.session.add(user_profile)
