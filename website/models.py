from flask_login import UserMixin
from website import db, bcrypt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)

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
