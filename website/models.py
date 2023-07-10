from flask_login import UserMixin
from website import db, bcrypt, app
from datetime import datetime
from sqlalchemy import JSON
from sqlalchemy.ext.mutable import MutableDict
from collections import OrderedDict
from werkzeug.utils import secure_filename
from os import path, remove


def default_timestamp() -> datetime:
    return datetime.utcnow()


class SearchHistory(db.Model):
    """Model representing the search history for a user."""

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    city = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)

    @property
    def time(self):
        return self.timestamp.strftime("%H:%M")

    @property
    def date(self):
        return self.timestamp.strftime("%d %B")


class User(UserMixin, db.Model):
    """Model representing a user."""

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    view_count = db.Column(MutableDict.as_mutable(JSON), nullable=False, default={})
    search_history = db.relationship(
        "SearchHistory", backref="user", cascade="all, delete", lazy=True
    )
    profile_pic = db.Column(db.String(), nullable=False, default="default.png")
    reset_token = db.Column(db.String(100))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, text_password: str):
        self.password_hash = bcrypt.generate_password_hash(
            password=text_password
        ).decode("utf-8")

    def check_password_correction(self, attempted_password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def update_username(self, new_username: str):
        self.username = new_username
        db.session.add(self)
        db.session.commit()

    def update_password(self, old_password: str, new_password: str):
        if self.check_password_correction(old_password):
            self.password = new_password
            db.session.add(self)
            db.session.commit()
        else:
            raise ValueError()

    def reset_password(self, new_password: str):
        self.password = new_password
        db.session.add(self)
        db.session.commit()

    def update_history(self, city: str):
        """Updates the user search history.

        Args:
            city (str): The city to add to the search history.
            date (str): The desirable date the users wanted to see the weather on.
        Returns:
            None
        """

        if city in self.view_count:
            self.view_count[city] += 1
        else:
            self.view_count[city] = 1

        search_entry = SearchHistory(city=city, user=self)

        db.session.add(search_entry)
        db.session.commit()

    def get_top_viewed_cities(self):
        sorted_dict = OrderedDict(
            sorted(self.view_count.items(), key=lambda x: x[1], reverse=True)
        )

        return sorted_dict

    def update_profile_pic(self, file):
        prev_profile_pic = self.profile_pic

        if prev_profile_pic != "default.png":
            prev_profile_pic_path = path.join(
                app.config["UPLOAD_PROFILE_FOLDER"], prev_profile_pic
            )
            try:
                remove(prev_profile_pic_path)
            except FileNotFoundError:
                pass

        filename = secure_filename(file.filename)
        file.save(path.join(app.config["UPLOAD_PROFILE_FOLDER"], filename))
        self.profile_pic = filename
        db.session.add(self)
        db.session.commit()
