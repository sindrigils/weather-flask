from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, EmailField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from website.models import User
from string import punctuation


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check: str):
        existing_username = User.query.filter_by(
            username=username_to_check.data
        ).first()

        if existing_username:
            raise ValidationError(
                message=f"This username '{username_to_check.data}' already exists! Please use another username."
            )

        if any(letter in punctuation for letter in username_to_check.data):
            raise ValidationError(message=f"No punctuation's are allowd in username!")

    def validate_email(self, email_to_check: str):
        existing_email = User.query.filter_by(email=email_to_check.data).first()

        if existing_email:
            raise ValidationError(
                message=f"This email '{email_to_check.data}' already exists! Please use another email."
            )

    username = StringField(
        label="Username", validators=[Length(min=2, max=30), DataRequired()]
    )
    email = EmailField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(
        label="Password", validators=[Length(min=7), DataRequired()]
    )
    retype_password = PasswordField(
        label="Re-enter Password",
        validators=[EqualTo("password", "Passwords don't match!"), DataRequired()],
    )
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")
