from flask import Flask

from celery import Celery


def create_celery(app: Flask) -> Celery:

    celery = Celery()
    celery.config_from_object(app.config, namespace='CELERY')

    class ContextTask(celery.Task):  # noqa: WPS431
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery()
    celery.config_from_object(app.config, namespace='CELERY')
    celery.Task = ContextTask
    return celery
