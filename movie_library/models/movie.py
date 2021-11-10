from movie_library import db
from movie_library.models import movie_genre


class Movie(db.Model):
    """Contains the properties and relationships of the movie"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Numeric(4, 2))
    description = db.Column(db.Text)
    preview = db.Column(db.String(100))
    budget = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    age_restriction_id = db.Column(db.Integer, db.ForeignKey('age_restriction.id'))
    genres = db.relationship('Genre', secondary=movie_genre,
                             backref=db.backref('movies'), lazy=True)

    def __repr__(self):
        return f'<Movie {self.title}>'
