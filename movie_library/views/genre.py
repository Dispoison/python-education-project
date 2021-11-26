"""Genre view module"""

from flask import request, abort
from flask_restx import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound

from movie_library import api, db
from movie_library.models import Genre, genre_model
from movie_library.schemes import GenreSchema
from movie_library.utils import admin_required, get_by_id_or_404, get_all_or_404, \
    add_model_object, update_model_object, delete_model_object, \
    log_error, log_info, log_object_info


genre_schema = GenreSchema()

genre_ns = api.namespace(name='Genre', path='/genres', description='genre methods')


@genre_ns.route('')
class GenresResource(Resource):
    """Genre plural resource"""

    @staticmethod
    @genre_ns.marshal_list_with(genre_model)
    def get():
        """Returns list of genre objects"""
        try:
            genres = get_all_or_404(Genre)

            log_info()
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return genres

    @staticmethod
    @admin_required
    @genre_ns.expect(genre_model)
    @genre_ns.marshal_with(genre_model, code=201, description='The genre was successfully created')
    def post():
        """Creates genre and returns deserialized object"""
        try:
            genre = genre_schema.load(request.json, session=db.session)
            add_model_object(genre)

            log_object_info(genre)
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return genre, 201


@genre_ns.route('/<int:genre_id>')
class GenreResource(Resource):
    """Genre singular resource"""

    @staticmethod
    @genre_ns.marshal_with(genre_model)
    def get(genre_id: int):
        """Returns genre object"""
        try:
            genre = get_by_id_or_404(Genre, genre_id)

            log_info()
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return genre

    @staticmethod
    @admin_required
    @genre_ns.expect(genre_model)
    @genre_ns.marshal_with(genre_model)
    def put(genre_id: int):
        """Updates genre and returns deserialized object"""
        try:
            genre = get_by_id_or_404(Genre, genre_id)

            genre = genre_schema.load(request.json, instance=genre,
                                      session=db.session, partial=True)
            update_model_object()

            log_object_info(genre)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return genre

    @staticmethod
    @admin_required
    @genre_ns.response(204, 'Successfully deleted')
    def delete(genre_id: int):
        """Deletes genre object"""
        try:
            genre = get_by_id_or_404(Genre, genre_id)

            delete_model_object(genre)

            log_object_info(genre)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return '', 204
