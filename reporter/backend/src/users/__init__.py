from flask import (
    Blueprint,
    render_template,
)

users = Blueprint('users', __name__, template_folder="templates")
# ,
# template_folder='templates',
# static_folder='static', static_url_path='assets')

from users import routes
