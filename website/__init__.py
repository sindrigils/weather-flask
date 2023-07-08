from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from website.env_loader import SECRET_KEY, MAIL_USERNAME, MAIL_PASSWORD
from os import path

UPLOAD_FOLDER = "static/images/profile-pics"

app: Flask = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["UPLOAD_PROFILE_FOLDER"] = path.join(app.root_path, UPLOAD_FOLDER)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_DEFAULT_SENDER"] = MAIL_USERNAME
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD


db: SQLAlchemy = SQLAlchemy(app)
bcrypt: Bcrypt = Bcrypt(app)
mail: Mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login_page"
login_manager.login_message_category = "info"


app.app_context().push()


from .views import views

app.register_blueprint(views, url_prefix="/")


from .auth import auth

app.register_blueprint(auth, url_prefix="/")

from .api_proxy import proxy

app.register_blueprint(proxy, url_prefix="/")

from website.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    pass
