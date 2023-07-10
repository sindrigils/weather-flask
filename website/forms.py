from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from website.models import User
from string import punctuation


class RegisterForm(FlaskForm):
    """
    Form for user registration.

    This form allows users to register by providing a username, email, password, and re-entering the password
    for confirmation. It includes validation methods to check for unique usernames and emails, as well as password
    match validation.

    Attributes:
        username (StringField): The field for entering the username.
        email (EmailField): The field for entering the email address.
        password (PasswordField): The field for entering the password.
        retype_password (PasswordField): The field for re-entering the password for confirmation.
        submit (SubmitField): The button for submitting the form.

    Methods:
        validate_username(username_to_check): Validates the uniqueness of the username.
        validate_email(email_to_check): Validates the uniqueness of the email address.

    """

    def validate_username(self, username_to_check: StringField):
        """
        Validate the uniqueness of the username.
        Checks if the provided username already exists in the database. If it exists, a validation error is raised.
        """

        existing_username = User.query.filter_by(
            username=username_to_check.data
        ).first()

        if existing_username:
            raise ValidationError(
                message=f"This username '{username_to_check.data}' already exists! Please use another username."
            )

        if any(letter in punctuation for letter in username_to_check.data):
            raise ValidationError(message=f"No punctuation's are allowd in username!")

    def validate_email(self, email_to_check: EmailField):
        """
        Validate the uniqueness of the email address.
        Checks if the provided email address already exists in the database. If it exists, a validation error is raised.
        """

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
    """
    Form for user login.

    This form allows users to log in by providing their email and password.

    Attributes:
        email (EmailField): The field for entering the email address.
        password (PasswordField): The field for entering the password.
        submit (SubmitField): The button for submitting the form.

    """

    email = EmailField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign in")


class ChangeUsernameForm(FlaskForm):
    """
    Form for changing the username.

    This form allows users to change their username by providing a new username and repeating it for confirmation.

    Attributes:
        new_username (StringField): The field for entering the new username.
        repeat_username (StringField): The field for repeating the new username for confirmation.
        submit_username (SubmitField): The button for submitting the form.

    """

    new_username = StringField(
        label="New Username", validators=[DataRequired(), Length(min=2, max=30)]
    )
    repeat_username = StringField(
        label="Repeat Username",
        validators=[EqualTo("new_username", "Username don't match"), DataRequired()],
    )
    submit_username = SubmitField(label="Change Username")


class ChangePasswordForm(FlaskForm):
    """
    Form for changing the password.

    This form allows users to change their password by providing the current password, a new password,
    and repeating the new password for confirmation.

    Attributes:
        old_password (PasswordField): The field for entering the current password.
        new_password (PasswordField): The field for entering the new password.
        repeat_new_password (PasswordField): The field for repeating the new password for confirmation.
        submit_password (SubmitField): The button for submitting the form.

    """

    old_password = PasswordField(label="Current Password", validators=[DataRequired()])
    new_password = PasswordField(
        label="New Password", validators=[DataRequired(), Length(min=7)]
    )
    repeat_new_password = PasswordField(
        label="Repeat Password",
        validators=[DataRequired(), EqualTo("new_password", "Passwords don't match!")],
    )
    submit_password = SubmitField(label="Change Password")


class DeleteAccountForm(FlaskForm):
    """
    Form for deleting the user account.

    This form allows users to delete their account by providing their username, email, and password.
    The user must enter their username, email, and password correctly to confirm the account deletion.

    Attributes:
        username (StringField): The field for entering the username.
        email (StringField): The field for entering the email.
        password (PasswordField): The field for entering the password.
        submit (SubmitField): The button for submitting the form.

    """

    username = StringField(label="Username", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Delete Account!")


class ResetPasswordForm(FlaskForm):
    """
    Form for resetting the user password.

    This form allows users to reset their password by entering a new password and confirming it.
    The new password should be at least 7 characters long, and the confirmation password should match the new password.

    Attributes:
        new_password (PasswordField): The field for entering the new password.
        repeat_new_password (PasswordField): The field for confirming the new password.
        submit (SubmitField): The button for submitting the form.

    """

    new_password = PasswordField(
        label="Password", validators=[DataRequired(), Length(min=7)]
    )
    repeat_new_password = PasswordField(
        label="Repeat Password",
        validators=[DataRequired(), EqualTo("new_password", "Passwords don't match!")],
    )
    submit = SubmitField(label="Reset Password")


class ContactForm(FlaskForm):
    text_area = TextAreaField(validators=[DataRequired()])
    submit = SubmitField(label="Submit")
