from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import FlaskConfig

app = Flask(import_name=__name__)
app.config.from_object(obj=FlaskConfig)
db = SQLAlchemy(app=app)
bcrypt = Bcrypt(app=app)

login_manager = LoginManager(app=app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
from trades import routes
