from celery import current_app
from flask import Flask


def create_celery_app(app:Flask):
    celery = current_app
    celery.config_from_object(app.config, namespace='CELERY')

    return celery
