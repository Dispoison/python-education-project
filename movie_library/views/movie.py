"""Movie view module"""

from flask import request, abort
from flask_restx import Resource
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound
from marshmallow.exceptions import ValidationError

from movie_library import api, db
from movie_library.models import Movie, movie_model_deserialize, movie_model_serialize
from movie_library.schemes import MovieSchema
from movie_library.utils import verify_ownership_by_user_id, OwnershipError, \
    get_by_id_or_404, add_model_object, update_model_object, delete_model_object, \
    log_error, log_info, log_object_info, parse_query_parameters

movie_schema = MovieSchema()

movie_ns = api.namespace(name='Movie', path='/movies', description='movie methods')


@movie_ns.route('')
class MoviesResource(Resource):
    """Movie plural resource"""

    @staticmethod
    @movie_ns.param('sort', 'Sort parameter [rating;release_date,asc]')
    @movie_ns.param('genres',
                    'Filter by genres (AND, case insensitive exact match) [Horror,thriller]')
    @movie_ns.param('directors',
                    'Filter by substring of directors\' full names (OR, ilike) [Quentin,luc bes]')
    @movie_ns.param('release_date_range', 'Filter by release date range [2003-01-01,2021-11-16]')
    @movie_ns.param('page_size', 'Number of movies on page (default: 10)', type=int)
    @movie_ns.param('page', 'Page number (default: 1)', type=int)
    @movie_ns.param('q', 'Movie title search substring')
    @movie_ns.marshal_list_with(movie_model_deserialize)
    def get():
        """Returns list of movie objects"""
        try:
            params = parse_query_parameters(request.args)

            movies = Movie.get_movies_by(params)

            log_info()
        except ValueError as error:
            log_error(error)
            return abort(400, str(error))
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return movies

    @staticmethod
    @login_required
    @movie_ns.expect(movie_model_serialize)
    @movie_ns.marshal_with(movie_model_deserialize, code=201,
                           description='The movie was successfully created')
    def post():
        """Creates movie and returns deserialized object"""
        try:
            genres_ids = Movie.cut_genres_ids_from_request_json(request.json)
            request.json['user_id'] = current_user.get_id()

            movie = movie_schema.load(request.json, session=db.session)

            if genres_ids is not None:
                movie.genres = Movie.get_genres_by_genres_ids(genres_ids)
                request.json['genres'] = genres_ids

            add_model_object(movie)

            log_object_info(movie)
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return movie, 201


@movie_ns.route('/<int:movie_id>')
class MovieResource(Resource):
    """Movie singular resource"""

    @staticmethod
    @movie_ns.marshal_with(movie_model_deserialize)
    def get(movie_id: int):
        """Returns movie object"""
        try:
            movie = get_by_id_or_404(Movie, movie_id)

            log_info()
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return movie

    @staticmethod
    @login_required
    @movie_ns.expect(movie_model_serialize)
    @movie_ns.marshal_with(movie_model_deserialize)
    def put(movie_id: int):
        """Updates movie and returns deserialized object"""
        try:
            movie = get_by_id_or_404(Movie, movie_id)
            verify_ownership_by_user_id(movie.user_id,
                                        'A movie can only be edited by the user who added it '
                                        'or by the administrator.')

            genres_ids = Movie.cut_genres_ids_from_request_json(request.json)

            movie = movie_schema.load(request.json, instance=movie,
                                      session=db.session, partial=True)
            if genres_ids is not None:
                movie.genres = Movie.get_genres_by_genres_ids(genres_ids)
                request.json['genres'] = genres_ids

            update_model_object()

            log_object_info(movie)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        except OwnershipError as error:
            log_error(error)
            return abort(403, str(error))
        else:
            return movie

    @staticmethod
    @login_required
    @movie_ns.response(204, 'Successfully deleted')
    def delete(movie_id: int):
        """Deletes movie object"""
        try:
            movie = get_by_id_or_404(Movie, movie_id)
            verify_ownership_by_user_id(movie.user_id,
                                        'A movie can only be deleted by the user who added it '
                                        'or by the administrator.')

            delete_model_object(movie)

            log_object_info(movie)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        except OwnershipError as error:
            log_error(error)
            return abort(403, str(error))
        else:
            return '', 204
