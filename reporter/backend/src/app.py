from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import FlaskConfig

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
login_manager.login_message_category = 'info'


def create_app(config: type[FlaskConfig] = FlaskConfig) -> Flask:
    app = Flask(import_name=__name__)
    app.config.from_object(obj=config)
    db.init_app(app=app)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)

    from trades import trades
    from users import users

    app.register_blueprint(users)
    app.register_blueprint(trades)

    return app