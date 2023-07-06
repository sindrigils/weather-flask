from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, login_user, logout_user, current_user
from website import db
from website.forms import (
    LoginForm,
    RegisterForm,
    ChangePasswordForm,
    ChangeUsernameForm,
    DeleteAccountForm,
)
from website.models import User
from website.utils.support import flash_errors


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login_page():
    """
    Route for handling user login.

    If the current user is already authenticated, they are redirected to the home page.
    Otherwise, the login form is created and validated on submit.
    If the form is validated and the login credentials are correct, the user is logged in
    and redirected to the home page with a success flash message.
    If the form is not validated or the login credentials are incorrect, an error flash message is shown.

    Returns:
        The redirect response if the user is logged in, or the rendered login page response.
    """

    if current_user.is_authenticated:
        flash(message=f"You're already logged in!", category="info")
        return redirect(url_for("views.home_page"))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(email=login_form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=login_form.password.data
        ):
            login_user(attempted_user)
            flash(message=f"Welcome back {attempted_user.username}", category="success")
            return redirect(url_for("views.home_page"))

        flash(
            message=f"Email and password don't match! Please try again.",
            category="danger",
        )
    return render_template("login-page.html", form=login_form)


@auth.route("register", methods=["POST", "GET"])
def register_page():
    """
    Register a new user.

    This route handles the registration process for a new user. It allows users to create an account by providing
    their desired username, email, and password. If the registration is successful, the user is redirected to the
    home page and a success message is displayed. If there are any validation errors with the registration form,
    corresponding error messages are flashed.

    Returns:
        If the registration is successful, redirects to the home page.
        If there are validation errors, renders the registration page with the corresponding error messages.

    """

    register_form = RegisterForm()

    if current_user.is_authenticated:
        flash(
            message=f"Log out first in order to create another account!",
            category="info",
        )
        return redirect(url_for("views.home_page"))

    if register_form.validate_on_submit():
        user_to_create = User(
            username=register_form.username.data,
            email=register_form.email.data,
        )
        user_to_create.password = register_form.password.data

        db.session.add(user_to_create)
        db.session.commit()
        flash(
            message=f"Account created successfully, welcome {user_to_create.username}!",
            category="info",
        )
        login_user(user_to_create)

        return redirect(url_for("views.home_page"))

    if register_form.errors != {}:
        flash_errors(register_form)

    return render_template("register-page.html", form=register_form)


@auth.route("/logout")
@login_required
def logout_page():
    """
    Log out the current user.

    This route logs out the current authenticated user. It calls the `logout_user` function provided by the Flask-Login
    extension to remove the user's session and clear the authentication state. After logging out, a flash message is
    displayed to inform the user, and they are redirected to the login page.

    Returns:
        A redirect response to the login page.

    """

    logout_user()
    flash(message=f"You have been logged out!", category="info")
    return redirect(url_for("auth.login_page"))


@auth.route("/settings", methods=["POST", "GET"])
@login_required
def settings_page():
    """
    Manage user settings.

    This route allows the user to manage their account settings. It provides forms for changing the username,
    changing the password, and deleting the account.

    If the change username form is submitted and valid, the user's username is updated to the new value and a success
    flash message is displayed. If the new username is the same as the current username, an info flash message is
    displayed.

    If the change password form is submitted and valid, the user's password is updated to the new value and a success
    flash message is displayed. If an error occurs during password update, a danger flash message is displayed.

    If the delete account form is submitted and valid, the user's account is deleted, they are logged out, and a success
    flash message is displayed.

    If there are validation errors in any of the forms, corresponding danger flash messages are displayed.

    Returns:
        A rendered template for the settings page.

    """

    change_username_form = ChangeUsernameForm()
    change_password_form = ChangePasswordForm()
    delete_account_form = DeleteAccountForm()

    if (
        change_username_form.validate_on_submit()
        and change_username_form.submit_username.data
    ):
        attempted_new_username = change_username_form.new_username.data

        if attempted_new_username == current_user.username:
            flash(message=f"This is already your username!", category="info")
        else:
            current_user.update_username(new_username=attempted_new_username)
            flash(
                message=f"You successfully changed your username to {current_user.username}",
                category="success",
            )

        return redirect(url_for("auth.settings_page"))

    elif (
        change_password_form.validate_on_submit()
        and change_password_form.submit_password.data
    ):
        try:
            current_user.update_password(
                old_password=change_password_form.old_password.data,
                new_password=change_password_form.new_password.data,
            )
            flash(message=f"Password has been changed", category="success")
        except ValueError:
            flash(message="Not successfull", category="danger")
        return redirect(url_for("auth.settings_page"))

    elif delete_account_form.validate_on_submit() and delete_account_form.submit.data:
        form_username = delete_account_form.username.data
        form_email = delete_account_form.email.data
        form_password = delete_account_form.password.data

        if form_username != current_user.username:
            flash(
                message=f"The username you entered doesn't match your account username!",
                category="danger",
            )
            return redirect(url_for("auth.settings_page"))

        if form_email != current_user.email:
            flash(
                message=f"The email you entered doesn't match your account email!",
                category="danger",
            )
            return redirect(url_for("auth.settings_page"))

        if not current_user.check_password_correction(form_password):
            flash(
                message=f"The password you enterd doesn't match your account password!",
                category="danger",
            )
            return redirect(url_for("auth.settings_page"))

        username = current_user.username
        email = current_user.email
        logout_user()

        account_to_delete = User.query.filter_by(username=username, email=email).first()
        db.session.delete(account_to_delete)
        db.session.commit()
        flash(
            message=f"Your account has been deleted successfully!", category="success"
        )

        return redirect(url_for("auth.login_page"))

    if change_username_form.errors != {} and change_username_form.submit_username.data:
        flash_errors(change_username_form)

    if change_password_form.errors != {} and change_password_form.submit_password.data:
        flash_errors(change_password_form)

    if delete_account_form.errors != {} and delete_account_form.submit.data:
        flash_errors(delete_account_form)

    return render_template(
        "settings-page.html",
        password_form=change_password_form,
        username_form=change_username_form,
        delete_form=delete_account_form,
    )
