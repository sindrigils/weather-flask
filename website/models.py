from flask_login import UserMixin
from website import db, bcrypt, app
from datetime import datetime
from sqlalchemy import JSON
from sqlalchemy.ext.mutable import MutableDict
from collections import OrderedDict
from werkzeug.utils import secure_filename
from os import path, remove

DEFAULT_PROFILE_PIC = "default.png"


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
    profile_pic = db.Column(db.String(), nullable=False, default=DEFAULT_PROFILE_PIC)
    reset_token = db.Column(db.String(100))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, text_password: str):
        """
        Setter for the password attribute.
        This method generates a password hash from the provided `text_password` and sets it as the `password_hash` attribute.

        Args:
            text_password (str): The plaintext password to set.
        """

        self.password_hash = bcrypt.generate_password_hash(
            password=text_password
        ).decode("utf-8")

    def check_password_correction(self, attempted_password: str) -> bool:
        """
        Checks if the attempted password matches the user's password.

        This function verifies whether the attempted password matches the user's stored password. It uses bcrypt to compare the hashed password stored in the `password_hash` attribute with the attempted password.

        Args:
            attempted_password (str): The password to check against the user's stored password.

        Returns:
            bool: True if the attempted password matches the user's password, False otherwise.
        """

        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def update_username(self, new_username: str):
        """
        Updates the user's username.

        This function updates the user's username with a new one. It sets the new username provided as the argument and updates the corresponding database entry.

        Args:
            new_username (str): The new username to set for the user.
        """

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
        """Resets the user's password.

        This function updates the user's password with a new one. It sets the new password provided
        as the argument and updates the corresponding database entry.

        Args:
            new_password (str): The new password to set for the user.
        """

        self.password = new_password
        db.session.add(self)
        db.session.commit()

    def update_history(self, city: str):
        """Updates the user search history.

        Args:
            city (str): The city to add to the search history.
            date (str): The desirable date the users wanted to see the weather on.
        """

        if city in self.view_count:
            self.view_count[city] += 1
        else:
            self.view_count[city] = 1

        search_entry = SearchHistory(city=city, user=self)

        db.session.add(search_entry)
        db.session.commit()

    def get_top_viewed_cities(self):
        """
        Returns a dictionary of the user's top viewed cities.

        This function retrieves the user's view count dictionary, which tracks the number of times each city has been viewed by the user.
        It sorts the dictionary in descending order based on the view count and returns the sorted dictionary.

        Returns:
            OrderedDict: A dictionary containing the user's top viewed cities, sorted by view count in descending order.
        """

        sorted_dict = OrderedDict(
            sorted(self.view_count.items(), key=lambda x: x[1], reverse=True)
        )

        return sorted_dict

    def update_profile_pic(self, file):
        """
        Updates the user's profile picture.

        This function replaces the user's current profile picture with a new one. If the user already has a profile picture other than the default one,
        the function removes the previous picture from the upload folder. The new picture is saved in the upload folder
        with a secure filename and its path is updated in the user's profile. The database entry is also updated accordingly.

        Args:
            file (FileStorage): The file object representing the new profile picture.
        """

        prev_profile_pic = self.profile_pic

        if prev_profile_pic != DEFAULT_PROFILE_PIC:
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

    def validate_profile_pic(self):
        """
        Validates the user's profile picture.
        This function checks if the user's profile picture exists in the specified upload folder.
        If the picture does not exist, it sets the profile picture to the default value and updates
        the corresponding database entry.
        """

        file_path = path.join(app.config["UPLOAD_PROFILE_FOLDER"], self.profile_pic)
        if not path.exists(file_path):
            self.profile_pic = DEFAULT_PROFILE_PIC
            db.session.add(self)
            db.session.commit()
