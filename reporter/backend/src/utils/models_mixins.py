from typing import TypeVar

from src import db

T = TypeVar('T', bound=db.Model)  # noqa: WPS111


class SaveMixin:
    def save(self) -> T:
        """Save object to db."""
        db.session.add(self)
        db.session.commit()
        return self
