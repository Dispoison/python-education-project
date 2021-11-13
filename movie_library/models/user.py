from datetime import datetime

from flask_login import UserMixin

from movie_library import db, login_manager


class User(db.Model, UserMixin):
    """Contains the properties and relationships of the user"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_activity = db.Column(db.DateTime, default=datetime.now())
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    movies = db.relationship('Movie', backref='user', lazy=True)

    def __init__(self, username, email, password, first_name, last_name):
        self.username = username
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'<{"Admin" if self.is_admin else "User"} {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
