from flask import (
    Blueprint,
    Flask,
)

from celery import current_app
from celery.local import Proxy

celery = Blueprint(name='celery', import_name=__name__)


def create_celery_app(app: Flask) -> Proxy:
    celery_app = current_app
    celery_app.config_from_object(app.config, namespace='CELERY')
    return celery_app
