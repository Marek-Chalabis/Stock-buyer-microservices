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
from users.forms import RegisterForm
from users.models import User


class RegisterView(View):
    methods = ['GET', 'POST']

    def __init__(self) -> None:
        self._form = RegisterForm()

    def dispatch_request(self) -> ResponseReturnValue:
        return (
            self._handle_correct_form_validation()
            if self._form.validate_on_submit()
            else self._handle_incorrect_form_validation()
        )

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
