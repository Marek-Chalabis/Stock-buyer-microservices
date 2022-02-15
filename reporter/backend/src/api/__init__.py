from flask import Blueprint

from api.v1 import api_v1

api = Blueprint('api', __name__, url_prefix='/api')

api.register_blueprint(api_v1)
