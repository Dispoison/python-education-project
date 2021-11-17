"""Director model module"""

from flask_restx import fields
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound

from movie_library import db, api


director_model = api.model('Director', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'description': fields.String(),
})
director_info_model = api.model('DirectorInfo', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(),
    'last_name': fields.String(),
})


class Director(db.Model):
    """Contains the properties and relationships of the director of the movie"""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    description = db.Column(db.Text)
    movies = db.relationship('Movie', backref='director', lazy=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Director \'{self.first_name} {self.last_name}\'>'

    @classmethod
    def get_directors_by(cls, search_data: str, page: int, page_size: int) -> list:
        """Returns searched, paginated directors"""
        director_query = cls.query

        if search_data:
            director_query = director_query.filter(func.concat(cls.first_name, ' ', cls.last_name).
                                                   ilike(f'%{search_data}%'))

        offset = page_size * (page - 1)
        directors = director_query.offset(offset).limit(page_size).all()

        if not directors:
            raise NoResultFound('No directors found.')

        return directors
