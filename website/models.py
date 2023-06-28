from flask_login import UserMixin
from website import db, bcrypt
from datetime import datetime
from sqlalchemy import JSON
from sqlalchemy.ext.mutable import MutableDict
from collections import OrderedDict


class SearchHistory(db.Model):
    """Model representing the search history for a user."""

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    city = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow())

    @property
    def time(self):
        return self.timestamp.strftime("%H:%M")


class User(UserMixin, db.Model):
    """Model representing a user."""

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    view_count = db.Column(MutableDict.as_mutable(JSON), nullable=False, default={})
    search_history = db.relationship("SearchHistory", backref="user", lazy=True)

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

    def update_history(self, city: str, date: str):
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

        search_entry = SearchHistory(city=city, date=date, user=self)

        db.session.add(search_entry)
        db.session.commit()

    def get_top_viewed_cities(self):
        sorted_dict = OrderedDict(
            sorted(self.view_count.items(), key=lambda x: x[1], reverse=True)
        )

        return sorted_dict
