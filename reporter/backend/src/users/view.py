from typing import Union

from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask.views import View
from flask_login import login_user

from app import db
from trades.forms import LoginForm
from users.forms import RegisterForm
from users.models import User


class RegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self._form = RegisterForm()

    def dispatch_request(self) -> ResponseReturnValue:
        if self._form.validate_on_submit():
            return self._handle_correct_form_validation()
        return self._handle_incorrect_form_validation()

    def _get_user_from_form(self) -> User:
        return User(
            username=self._form.username.data,
            email=self._form.email.data,
            password=self._form.password.data,
        )

    def _handle_correct_form_validation(self) -> ResponseReturnValue:
        user_to_create = self._get_user_from_form()
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user=user_to_create)
        # TODO add link to add money and change redirect template for trades
        flash(
            f'Account {user_to_create.username} created successfully',
            category='success',
        )

        return redirect(location=url_for(endpoint='users.home_page'))

    def _handle_incorrect_form_validation(self) -> ResponseReturnValue:
        if self._form.errors:
            for err_msg in self._form.errors.values():
                flash(*err_msg, category='danger')
        return render_template(template_name_or_list='register.html', form=self._form)


class LoginView(View):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self._form = LoginForm()

    def dispatch_request(self) -> ResponseReturnValue:
        if self._form.validate_on_submit():
            return self._handle_correct_form_validation()
        return render_template(template_name_or_list='login.html', form=self._form)

    def _handle_correct_form_validation(self) -> ResponseReturnValue:
        user = self._get_user_from_form()
        if user and user.verify_password(password=self._form.password.data):
            return self._handle_correct_user(user=user)
        return self._handle_incorrect_user()

    def _get_user_from_form(self) -> Union[User, None]:
        return User.query.filter_by(username=self._form.username.data).scalar()

    def _handle_correct_user(self, user: User) -> ResponseReturnValue:
        login_user(user=user)
        flash(f'Welcome: {user.username}', category='success')
        # TODO change redirect template for trades
        return redirect(location=url_for(endpoint='users.home_page'))

    def _handle_incorrect_user(self) -> ResponseReturnValue:
        flash('Wrong username or password', category='danger')
        return render_template(template_name_or_list='login.html', form=self._form)
