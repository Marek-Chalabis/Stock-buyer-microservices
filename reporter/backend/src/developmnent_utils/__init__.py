from flask import (
    Blueprint,
    Flask,
)

development_utils = Blueprint(name='development_utils', import_name=__name__)


def is_development_mode(app_to_check: Flask) -> bool:
    if app_to_check.config['FLASK_ENV'] != 'development':
        print('App not in development state.')  # noqa: WPS421
        return False
    return True


from src.developmnent_utils import commands
