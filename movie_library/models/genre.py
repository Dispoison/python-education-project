from movie_library import db
from movie_library.models import movie_genre


class Genre(db.Model):
    """Contains the properties and relationships of the genre of the movie"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    movies = db.relationship('Movie', secondary=movie_genre,
                             backref=db.backref('genres'), lazy=True)

    def __repr__(self):
        return f'<Genre {self.title}>'
