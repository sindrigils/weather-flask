from flask_wtf import FlaskForm
from flask import flash
from secrets import token_hex


def flash_errors(form: FlaskForm):
    """
    Flash error messages for a form.

    Args:
        form: The form containing validation errors.

    """

    for error_msg in form.errors.values():
        flash(message=f"{error_msg[0]}", category="danger")


def generate_token() -> str:
    return token_hex(16)
