"""Director view module"""

from flask import request, abort
from flask_restx import Resource
from sqlalchemy.exc import NoResultFound
from marshmallow.exceptions import ValidationError

from movie_library import api, db
from movie_library.models import Director, director_model
from movie_library.schemes import DirectorSchema
from movie_library.utils import admin_required, add_model_object, \
    update_model_object, delete_model_object

director_schema = DirectorSchema()

director_ns = api.namespace(name='Director', path='/directors', description='director methods')


@director_ns.route('')
class DirectorsResource(Resource):
    """Director plural resource"""

    @director_ns.param('page_size', 'Number of directors on page (default: 10)', type=int)
    @director_ns.param('page', 'Page number (default: 1)', type=int)
    @director_ns.param('q', 'Searching for a director using a substring of the full name')
    @director_ns.marshal_list_with(director_model)
    def get(self):
        """Returns list of director objects"""
        try:
            params = Director.parse_query_parameters(request.args)

            directors = Director.get_directors_by(params)
        except ValueError as value_error:
            return abort(400, str(value_error))
        except NoResultFound as not_found:
            return abort(404, str(not_found))
        return directors

    @admin_required
    @director_ns.expect(director_model)
    @director_ns.marshal_with(director_model, code=201,
                              description='The director was successfully created')
    def post(self):
        """Creates director and returns deserialized object"""
        try:
            director = director_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return abort(422, error.messages)
        else:
            add_model_object(director)
            return director, 201


@director_ns.route('/<int:director_id>')
class DirectorResource(Resource):

    """Director singular resource"""

    @director_ns.marshal_with(director_model)
    def get(self, director_id: int):
        """Returns director object"""
        return Director.query.get_or_404(director_id)

    @admin_required
    @director_ns.expect(director_model)
    @director_ns.marshal_with(director_model)
    def put(self, director_id: int):
        """Updates director and returns deserialized object"""
        director = Director.query.get_or_404(director_id)
        try:
            director = director_schema.load(request.json, instance=director,
                                            session=db.session, partial=True)
        except ValidationError as error:
            return abort(422, error.messages)
        else:
            update_model_object(director)
            return director

    @admin_required
    @director_ns.response(204, 'Successfully deleted')
    def delete(self, director_id: int):
        """Deletes director object"""
        director = Director.query.get_or_404(director_id)
        delete_model_object(director)
        return '', 204
