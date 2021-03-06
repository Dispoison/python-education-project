"""Genre model module"""

from flask_restx import fields

from movie_library import db, api


genre_model = api.model('Genre', {
    'id': fields.Integer(readonly=True),
    'title': fields.String(),
})


class Genre(db.Model):
    """Contains the properties and relationships of the genre of the movie"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Genre \'{self.id}.{self.title}\'>'
