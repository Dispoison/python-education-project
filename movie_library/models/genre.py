from movie_library import db


class Genre(db.Model):
    """Contains the properties and relationships of the genre of the movie"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    def __repr__(self):
        return f'<Genre {self.title}>'
