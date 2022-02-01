import wtforms

from flask_wtf import FlaskForm
from wtforms import ValidationError

from users.models import User


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
                'password', message='Passwords are not identical'
            ),
        ],
    )
    submit = wtforms.SubmitField(label='Create Account')

    def validate_username(self, username_to_validate: wtforms.StringField) -> None:
        user_with_username_exists = User.query.filter_by(
            username=username_to_validate.data
        ).scalar()
        if user_with_username_exists:
            raise ValidationError('Username already exists. Try different username')

    def validate_email(self, email_to_validate: wtforms.StringField) -> None:
        user_with_email_exists = User.query.filter_by(
            email=email_to_validate.data
        ).scalar()
        if user_with_email_exists:
            raise ValidationError('Email already exists. Try different email')
