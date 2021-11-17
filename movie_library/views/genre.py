from flask import request
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import Genre, genre_model
from movie_library.schema import GenreSchema
from movie_library.utils import admin_required, get_all_or_404, \
    add_model_object, update_model_object, delete_model_object


genre_schema = GenreSchema()

genre_ns = api.namespace(name='Genre', path='/genres', description='genre methods')


@genre_ns.route('')
class GenresResource(Resource):
    @genre_ns.marshal_list_with(genre_model)
    def get(self):
        return get_all_or_404(Genre, 'No genres found.')

    @admin_required
    @genre_ns.expect(genre_model)
    @genre_ns.marshal_with(genre_model, code=201, description='The genre was successfully created')
    def post(self):
        genre = genre_schema.load(request.json, session=db.session)
        return add_model_object(genre)


@genre_ns.route('/<int:genre_id>')
class GenreResource(Resource):
    @genre_ns.marshal_with(genre_model)
    def get(self, genre_id):
        return Genre.query.get_or_404(genre_id)

    @admin_required
    @genre_ns.expect(genre_model)
    @genre_ns.marshal_with(genre_model)
    def put(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        genre = genre_schema.load(request.json, instance=genre, session=db.session, partial=True)
        return update_model_object(genre)

    @admin_required
    @genre_ns.response(204, 'Successfully deleted')
    def delete(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        return delete_model_object(genre)
