from typing import Union

from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from flask.typing import ResponseReturnValue
from flask.views import View
from flask_login import (
    current_user,
    login_required,
    login_user,
)

from users.enums import MoneyOperation
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
            template_name_or_list='register.html',
            form=self._register_form,
        )

    def _handle_correct_register_form(self) -> ResponseReturnValue:
        created_user = User(
            username=self._register_form.username.data,
            email=self._register_form.email.data,
            password=self._register_form.password.data,
        ).save()
        login_user(user=created_user)
        flash(
            f'Account {created_user.username} created successfully',
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
        self._user = current_user

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
            amount = self._money_form.amount.data
            operation = self._money_form.operation.data
            self._user.user_profile.update_money_by_amount(
                amount=(
                    f'{"-" if operation == MoneyOperation.PAY_OUT.value else ""}'
                    + f'{amount}'
                ),
                commit=True,
            )
            action = (
                'paid outed' if operation == MoneyOperation.PAY_OUT else 'deposited'
            )
            flash(message=f'Successfully {action} ${amount}', category='success')
        else:
            flash_errors_from_form(form=self._money_form)
