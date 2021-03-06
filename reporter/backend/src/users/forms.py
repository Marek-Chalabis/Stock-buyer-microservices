import flask_login
import wtforms

from flask_wtf import FlaskForm

from src.users.enums import MoneyOperation
from src.users.models import User
from src.utils.type_parsers import change_to_decimal


class RegisterForm(FlaskForm):
    username = wtforms.StringField(
        label='Username:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=2, max=30),
        ],
    )
    email = wtforms.StringField(
        label='Email:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Email(),
        ],
    )
    password = wtforms.PasswordField(
        label='Password:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.Length(min=6),
        ],
    )
    password_confirm = wtforms.PasswordField(
        label='Confirm Password:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.EqualTo(
                'password',
                message='Passwords are not identical',
            ),
        ],
    )
    submit = wtforms.SubmitField(label='Create Account')

    def validate_username(self, username_to_validate: wtforms.StringField) -> None:
        user_with_username_exists = User.query.filter_by(
            username=username_to_validate.data,
        ).scalar()
        if user_with_username_exists:
            raise wtforms.ValidationError(
                'Username already exists. Try different username',
            )

    def validate_email(self, email_to_validate: wtforms.StringField) -> None:
        user_with_email_exists = User.query.filter_by(
            email=email_to_validate.data,
        ).scalar()
        if user_with_email_exists:
            raise wtforms.ValidationError('Email already exists. Try different email')


class LoginForm(FlaskForm):
    username = wtforms.StringField(
        label='Username:',
        validators=[
            wtforms.validators.DataRequired(),
        ],
    )
    password = wtforms.PasswordField(
        label='Password:',
        validators=[
            wtforms.validators.DataRequired(),
        ],
    )
    submit = wtforms.SubmitField(label='Sign in')


class MoneyForm(FlaskForm):
    amount = wtforms.DecimalField(
        label='Amount:',
        validators=[
            wtforms.validators.DataRequired(),
            wtforms.validators.NumberRange(min=1, max=500000),
        ],
    )
    operation = wtforms.SelectField(
        label='Operation:',
        validators=[
            wtforms.validators.DataRequired(),
        ],
        choices=[choice.value for choice in MoneyOperation],
    )
    submit_money = wtforms.SubmitField(label='Transfer')

    def validate_amount(self, amount_to_validate: wtforms.DecimalField) -> None:
        if self.data['operation'] == MoneyOperation.PAY_OUT.value:
            user_money = change_to_decimal(flask_login.current_user.user_profile.money)
            if user_money < amount_to_validate.data:
                raise wtforms.ValidationError(
                    'You are trying to pay out more then you have',
                )
