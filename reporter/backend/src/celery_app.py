from celery import current_app
from celery.local import Proxy
from flask import Flask


def create_celery_app(app:Flask) -> Proxy:
    celery = current_app
    celery.config_from_object(app.config, namespace='CELERY')

    return celery
