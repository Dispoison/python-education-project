"""Movie model module"""

from datetime import datetime
from typing import Union, List

from flask_restx import fields
from sqlalchemy import func, or_, case
from sqlalchemy.exc import NoResultFound

from movie_library import db, api
from movie_library.models import movie_genre, Director, Genre, director_info_model, \
    genre_model, user_info_model, country_model, age_restriction_model
from movie_library.utils import get_order_objects_list

VALID_SORTING_VALUES = ('rating', 'release_date')
MIN_DATE = datetime.min
MAX_DATE = datetime.max

movie_base_model = api.model('MovieBase', {
    'title': fields.String(),
    'release_date': fields.DateTime(),
    'duration': fields.Integer(),
    'rating': fields.Float(),
    'description': fields.String(),
    'preview': fields.String(),
    'budget': fields.Float(),
})
movie_model_deserialize = api.clone('MovieDeserialize', movie_base_model, {
    'id': fields.Integer(readonly=True),
    'user': fields.Nested(user_info_model, readonly=True),
    'country': fields.Nested(country_model, readonly=True),
    'age_restriction': fields.Nested(age_restriction_model, readonly=True),
    'director': fields.Nested(director_info_model, readonly=True, default='unknown'),
    'genres': fields.List(fields.Nested(genre_model)),
})
movie_model_serialize = api.clone('MovieSerialize', movie_base_model, {
    'country_id': fields.Integer(default=1),
    'age_restriction_id': fields.Integer(default=1),
    'director_id': fields.Integer(default=1),
    'genres': fields.List(fields.Integer(default=1)),
})


class Movie(db.Model):
    """Contains the properties and relationships of the movie"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Numeric(4, 2))
    description = db.Column(db.Text)
    preview = db.Column(db.String(255))
    budget = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    age_restriction_id = db.Column(db.Integer, db.ForeignKey('age_restriction.id'))
    genres = db.relationship('Genre', secondary=movie_genre,
                             backref=db.backref('movies'), lazy=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Movie \'{self.title}\'>'

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
    def get_movies_by(cls, params: dict) -> list:
        """Returns searched, paginated, sorted and filtered movies"""
        movie_query = cls.query

        if params.get('sort'):
            sort_data = params['sort'].split(';')
            order_by = get_order_objects_list(sort_data, cls, VALID_SORTING_VALUES)
            movie_query = movie_query.order_by(*order_by)

        if params.get('q'):
            movie_query = movie_query.filter(cls.title.ilike(f'%{params["q"]}%'))

        if params.get('release_date_range'):
            date_range = params['release_date_range'].split(',')

            date_range[0] = MIN_DATE if date_range[0] == '' \
                else datetime.strptime(date_range[0], '%Y-%m-%d')
            date_range[1] = MAX_DATE if date_range[1] == '' \
                else datetime.strptime(date_range[1], '%Y-%m-%d')

            movie_query = movie_query.filter(Movie.release_date.between(*date_range))

        if params.get('directors'):
            directors = params['directors'].split(',')
            directors_conditions = [func.concat(Director.first_name, ' ',
                                                Director.last_name).ilike(f'%{director}%')
                                    for director in directors]
            movie_query = movie_query.join(Movie.director).filter(or_(*directors_conditions))

        if params.get('genres'):
            genres = params['genres'].split(',')
            genres = list(map(str.lower, genres))
            movie_query = movie_query. \
                join(movie_genre, Movie.id == movie_genre.c.movie_id). \
                join(Genre, movie_genre.c.genre_id == Genre.id). \
                group_by(Movie.id). \
                having(func.sum(case((func.lower(Genre.title).
                                      in_(genres), 1), else_=0)) == len(genres))

        offset = params['page_size'] * (params['page'] - 1)
        movies = movie_query.offset(offset).limit(params['page_size']).all()

        if not movies:
            raise NoResultFound('No movies found.')

        return movies

    @staticmethod
    def cut_genres_ids_from_request_json(request_json: dict) -> Union[list, None]:
        """Cuts genres_ids from request.json if exist else return None"""
        genres_ids = None
        if 'genres' in request_json:
            genres_ids = request_json.get('genres')

            from movie_library.schemes import MovieSchema
            MovieSchema.validate_genres_ids(genres_ids)

            del request_json['genres']
        return genres_ids

    @staticmethod
    def get_genres_by_genres_ids(genres_ids: List[int]) -> list:
        """Returns genres by genres_ids if genres_ids else []"""
        return Genre.query.filter(Genre.id.in_(genres_ids)).all() if genres_ids else []
