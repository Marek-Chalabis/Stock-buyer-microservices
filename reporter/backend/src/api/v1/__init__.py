from flask import Blueprint


api_v1 = Blueprint('api_v1', __name__, url_prefix='/v1')

from api.v1 import routes
