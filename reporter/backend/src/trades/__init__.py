from flask import Blueprint

trades = Blueprint('trades', __name__, template_folder='templates')

from src.trades import (
    routes,
    signals,
)
