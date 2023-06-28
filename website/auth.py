from flask import render_template, redirect, url_for, Blueprint, flash
from flask_login import login_required, login_user, logout_user, current_user
from website import db
from website.forms import LoginForm, RegisterForm
from website.models import User


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login_page():
    if current_user.is_authenticated:
        flash(message=f"You're already logged in!", category="info")
        return redirect(url_for("views.home_page"))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=login_form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=login_form.password.data
        ):
            login_user(attempted_user)
            flash(message=f"Welcome back {attempted_user.username}", category="success")
            return redirect(url_for("views.home_page"))

        flash(
            message=f"Username and password don't match! Please try again.",
            category="danger",
        )
    return render_template("login-page.html", form=login_form)


@auth.route("register", methods=["POST", "GET"])
def register_page():
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
        for error_msg in register_form.errors.values():
            flash(
                message=f"{error_msg[0]}",
                category="danger",
            )

    return render_template("register-page.html", form=register_form)


@auth.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash(message=f"You have been logged out!", category="info")
    return redirect(url_for("auth.login_page"))
