from flask import flash
from flask_wtf import FlaskForm


def flash_errors_from_form(form: FlaskForm) -> None:
    if form.errors:
        for err_msg in form.errors.values():
            flash(*err_msg, category='danger')
