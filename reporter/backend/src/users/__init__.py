from flask import Blueprint

users = Blueprint('users', __name__, template_folder='templates')

from src.users import (
    routes,
    signals,
)
