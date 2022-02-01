from typing import Union

from flask import render_template

from app import login_manager
from users import users
from users.models import User
from users.view import (
    LoginView,
    RegisterView,
)


@login_manager.user_loader
def load_user(user_id: str) -> Union[User, None]:
    return User.query.get(int(user_id))


@users.route('/')
@users.route('/home')
def home_page() -> str:
    return render_template(template_name_or_list='home.html')


users.add_url_rule('/register', view_func=RegisterView.as_view('register_page'))
users.add_url_rule('/login', view_func=LoginView.as_view('login_page'))
