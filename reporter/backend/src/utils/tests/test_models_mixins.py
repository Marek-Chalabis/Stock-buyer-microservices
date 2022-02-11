from app import db
from utils.models_mixins import SaveMixin


class SaveMixinConcrete(SaveMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)


class TestSaveMixin:
    def test_save(self):
        tested_object = SaveMixinConcrete()
        tested_object.save()
        tested_object_from_db = db.session.query(SaveMixinConcrete).scalar()
        assert tested_object_from_db
        assert tested_object == tested_object_from_db
