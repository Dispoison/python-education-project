from movie_library import db


class User(db.Model):
    """Contains the properties and relationships of the user"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime, server_default=db.func.now())
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f'<{"Admin" if self.is_admin else "User"} {self.username}>'
