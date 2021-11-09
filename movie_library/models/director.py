from movie_library import db


class Director(db.Model):
    """Contains the properties and relationships of the director of the movie"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    description = db.Column(db.Text)
    movies = db.relationship('Movie', backref='director', lazy=True)

    def __repr__(self):
        return f'<Director {self.first_name} {self.last_name}>'
