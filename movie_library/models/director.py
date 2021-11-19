"""Director model module"""

from flask_restx import fields
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound

from movie_library import db, api


director_model = api.model('Director', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(default='Name'),
    'last_name': fields.String(default='Surname'),
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
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    movies = db.relationship('Movie', backref='director', lazy=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Director \'{self.first_name} {self.last_name}\'>'

    @staticmethod
    def parse_query_parameters(args: dict) -> dict:
        params = dict(args)
        page = params.get('page', 1)
        page_size = params.get('page_size', 10)

        if isinstance(page, str) and not page.isdigit():
            raise ValueError('Parameter page must be positive integer.')
        params['page'] = int(page)

        if isinstance(page_size, str) and not page_size.isdigit():
            raise ValueError('Parameter page_size must be positive integer.')
        params['page_size'] = int(page_size)

        if params['page'] < 1:
            raise ValueError('Parameter page must be greater than 0.')
        if params['page_size'] < 1:
            raise ValueError('Parameter page_size must be greater than 0.')

        if params['page_size'] > 50:
            raise ValueError('Parameter page_size maximum value is 50.')

        return params

    @classmethod
    def get_directors_by(cls, params: dict) -> list:
        """Returns searched, paginated directors"""
        director_query = cls.query

        if params.get('q'):
            director_query = director_query.filter(func.concat(cls.first_name, ' ', cls.last_name).
                                                   ilike(f'%{params["q"]}%'))

        offset = params['page_size'] * (params['page'] - 1)
        directors = director_query.offset(offset).limit(params['page_size']).all()

        if not directors:
            raise NoResultFound('No directors found.')

        return directors
