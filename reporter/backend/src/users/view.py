from typing import Union

import flask_login

from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask.views import View
from flask_login import (
    login_required,
    login_user,
)

from users.forms import (
    LoginForm,
    MoneyForm,
    RegisterForm,
)
from users.models import User
from utils.view_utils import flash_errors_from_form


class RegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self._register_form = RegisterForm()

    def dispatch_request(self) -> ResponseReturnValue:
        if self._register_form.validate_on_submit():
            return self._handle_correct_register_form()
        else:
            flash_errors_from_form(form=self._register_form)
        return render_template(
            template_name_or_list='register.html', form=self._register_form
        )

    def _handle_correct_register_form(self) -> ResponseReturnValue:
        user_to_create = User.create(
            username=self._register_form.username.data,
            email=self._register_form.email.data,
            password=self._register_form.password.data,
        )
        login_user(user=user_to_create)
        flash(
            f'Account {user_to_create.username} created successfully',
            category='success',
        )
        return redirect(location=url_for(endpoint='trades.trades_page'))


class LoginView(View):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self._form = LoginForm()

    def dispatch_request(self) -> ResponseReturnValue:
        if self._form.validate_on_submit():
            user = self._get_user_from_form()
            if user and user.verify_password(password=self._form.password.data):
                return self._handle_correct_user(user=user)
            else:
                flash('Wrong username or password', category='danger')
        return render_template(template_name_or_list='login.html', form=self._form)

    def _get_user_from_form(self) -> Union[User, None]:
        return User.query.filter_by(username=self._form.username.data).scalar()

    def _handle_correct_user(self, user: User) -> ResponseReturnValue:
        login_user(user=user)
        flash(f'Welcome: {user.username}', category='success')
        return redirect(location=url_for(endpoint='trades.trades_page'))


class ProfileView(View):
    methods = ['GET', 'POST']
    decorators = [login_required]

    def __init__(self) -> None:
        self._money_form = MoneyForm()
        self._user = flask_login.current_user

    def dispatch_request(self) -> ResponseReturnValue:
        """Process correct form based on unique form submit field."""
        if self._money_form.submit_money.data:
            self._handle_money_form()
        return render_template(
            template_name_or_list='profile.html',
            money_form=self._money_form,
        )

    def _handle_money_form(self) -> None:
        if self._money_form.validate_on_submit():
            self._user.user_profile.change_money_based_on_operation(
                amount=self._money_form.amount.data,
                operation=self._money_form.operation,
            )
        else:
            flash_errors_from_form(form=self._money_form)
