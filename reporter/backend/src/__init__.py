from typing import Type

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from src.config import BaseConfig

db = SQLAlchemy()


bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = 'info'


def create_app(config: Type[BaseConfig] = BaseConfig) -> Flask:
    app = Flask(import_name=__name__)
    app.config.from_object(obj=config)
    db.init_app(app=app)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)

    from src.api import api
    from src.trades import trades
    from src.users import users

    app.register_blueprint(api)
    app.register_blueprint(users)
    app.register_blueprint(trades)

    # adds development utils
    from src.developmnent_utils import (
        development_utils,
        is_development_mode,
    )

    if is_development_mode(app_to_check=app):
        app.register_blueprint(development_utils)

    return app
