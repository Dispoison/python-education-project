from flask import request, abort
from flask_restx import Resource
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound

from movie_library import api, db
from movie_library.models import Movie, movie_model_deserialize, movie_model_serialize
from movie_library.schema import MovieSchema
from movie_library.utils import verify_ownership_by_user_id, add_model_object, update_model_object, delete_model_object


movie_schema = MovieSchema()

movie_ns = api.namespace(name='Movie', path='/movies', description='movie methods')


@movie_ns.route('')
class MoviesResource(Resource):
    @movie_ns.param('sort', 'Sort parameter [rating;release_date,asc]')
    @movie_ns.param('genres', 'Filter by genres (AND, case insensitive exact match) [Horror,thriller]')
    @movie_ns.param('directors', 'Filter by substring of directors\' full names (OR, ilike) [Quentin,luc bes]')
    @movie_ns.param('release_date_range', 'Filter by release date range [2003-01-01,2021-11-16]')
    @movie_ns.param('page_size', 'Number of movies on page (default: 10)')
    @movie_ns.param('page', 'Page number (default: 1)')
    @movie_ns.param('q', 'Movie title search substring')
    @movie_ns.marshal_list_with(movie_model_deserialize)
    def get(self):
        try:
            search_data = request.args.get('q')
            sort_data = request.args.get('sort')
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))
            release_date_range = request.args.get('release_date_range')
            directors = request.args.get('directors')
            genres = request.args.get('genres')

            movies = Movie.get_movies_by(search_data, sort_data, page, page_size, release_date_range, directors, genres)
        except ValueError as value_error:
            return abort(400, str(value_error))
        except NoResultFound as not_found:
            return abort(404, str(not_found))
        return movies

    @login_required
    @movie_ns.expect(movie_model_serialize)
    @movie_ns.marshal_with(movie_model_deserialize, code=201, description='The movie was successfully created')
    def post(self):
        genres = Movie.cut_genres_from_request_json(request.json)

        request.json['user_id'] = current_user.get_id()

        movie = movie_schema.load(request.json, session=db.session)

        if genres is not None:
            movie.genres = genres

        return add_model_object(movie)


@movie_ns.route('/<int:movie_id>')
class MovieResource(Resource):
    @movie_ns.marshal_with(movie_model_deserialize)
    def get(self, movie_id):
        return Movie.query.get_or_404(movie_id)

    @login_required
    @movie_ns.expect(movie_model_serialize)
    @movie_ns.marshal_with(movie_model_deserialize)
    def put(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        verify_ownership_by_user_id(movie.user_id, 'A movie can only be edited by the user who added it '
                                                   'or by the administrator.')

        genres = Movie.cut_genres_from_request_json(request.json)

        movie = movie_schema.load(request.json, instance=movie, session=db.session, partial=True)

        if genres is not None:
            movie.genres = genres

        return update_model_object(movie)

    @login_required
    @movie_ns.response(204, 'Successfully deleted')
    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        verify_ownership_by_user_id(movie.user_id, 'A movie can only be deleted by the user who added it '
                                                   'or by the administrator.')
        return delete_model_object(movie)
