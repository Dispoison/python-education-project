from flask import request, abort
from flask_restx import Resource
from sqlalchemy.exc import NoResultFound

from movie_library import api, db
from movie_library.models import Director, director_model
from movie_library.schema import DirectorSchema
from movie_library.utils import admin_required, add_model_object, update_model_object, delete_model_object


director_schema = DirectorSchema()

director_ns = api.namespace(name='Director', path='/directors', description='director methods')


@director_ns.route('')
class DirectorsResource(Resource):
    @director_ns.param('page_size', 'Number of movies on page (default: 10)')
    @director_ns.param('page', 'Page number (default: 1)')
    @director_ns.param('q', 'Searching for a director using a substring of the full name')
    @director_ns.marshal_list_with(director_model)
    def get(self):
        try:
            search_data = request.args.get('q')
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))

            directors = Director.get_directors_by(search_data, page, page_size)
        except ValueError as value_error:
            return abort(400, str(value_error))
        except NoResultFound as not_found:
            return abort(404, str(not_found))
        return directors

    @admin_required
    @director_ns.expect(director_model)
    @director_ns.marshal_with(director_model, code=201, description='The director was successfully created')
    def post(self):
        director = director_schema.load(request.json, session=db.session)
        return add_model_object(director)


@director_ns.route('/<int:director_id>')
class DirectorResource(Resource):
    @director_ns.marshal_with(director_model)
    def get(self, director_id):
        return Director.query.get_or_404(director_id)

    @admin_required
    @director_ns.expect(director_model)
    @director_ns.marshal_with(director_model)
    def put(self, director_id):
        director = Director.query.get_or_404(director_id)
        director = director_schema.load(request.json, instance=director, session=db.session, partial=True)
        return update_model_object(director)

    @admin_required
    @director_ns.response(204, 'Successfully deleted')
    def delete(self, director_id):
        director = Director.query.get_or_404(director_id)
        return delete_model_object(director)
