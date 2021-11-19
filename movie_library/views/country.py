"""Country view module"""

from flask import request, abort
from flask_restx import Resource
from marshmallow.exceptions import ValidationError

from movie_library import api, db
from movie_library.models import Country, country_model
from movie_library.schemes import CountrySchema
from movie_library.utils import admin_required, get_all_or_404, \
    add_model_object, update_model_object, delete_model_object


country_schema = CountrySchema()

country_ns = api.namespace(name='Country', path='/countries', description='country methods')


@country_ns.route('')
class CountriesResource(Resource):
    """Country plural resource"""

    @country_ns.marshal_list_with(country_model)
    def get(self):
        """Returns list of country objects"""
        return get_all_or_404(Country, 'No countries found.')

    @admin_required
    @country_ns.expect(country_model)
    @country_ns.marshal_with(country_model, code=201,
                             description='The country was successfully created')
    def post(self):
        """Creates country and returns deserialized object"""
        try:
            country = country_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return abort(422, error.messages)
        else:
            add_model_object(country)
            return country, 201


@country_ns.route('/<int:country_id>')
class CountryResource(Resource):
    """Country singular resource"""

    @country_ns.marshal_with(country_model)
    def get(self, country_id: int):
        """Returns country object"""
        return Country.query.get_or_404(country_id)

    @admin_required
    @country_ns.expect(country_model)
    @country_ns.marshal_with(country_model)
    def put(self, country_id: int):
        """Updates country and returns deserialized object"""
        country = Country.query.get_or_404(country_id)
        try:
            country = country_schema.load(request.json,
                                          instance=country,
                                          session=db.session,
                                          partial=True)
        except ValidationError as error:
            return abort(422, error.messages)
        else:
            update_model_object(country)
            return country

    @admin_required
    @country_ns.response(204, 'Successfully deleted')
    def delete(self, country_id: int):
        """Deletes country object"""
        country = Country.query.get_or_404(country_id)
        delete_model_object(country)
        return '', 204
