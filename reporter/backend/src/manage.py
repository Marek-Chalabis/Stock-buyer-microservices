from flask import Flask
from flask.cli import FlaskGroup

from app import create_app

app = create_app()
cli = FlaskGroup(app)


def is_development_mode(app_to_check: Flask) -> bool:
    if app_to_check.config['FLASK_ENV'] != 'development':
        print('App not in development state.')  # noqa: WPS421
        return False
    return True


# adds development utils
if is_development_mode(app_to_check=app):
    from commands_development import *

if __name__ == '__main__':
    cli()
