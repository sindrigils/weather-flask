from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from website.env_loader import secret_key
from os import path


app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
UPLOAD_FOLDER = "static/images/profile-pics"
app.config["UPLOAD_PROFILE_FOLDER"] = path.join(app.root_path, UPLOAD_FOLDER)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

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
