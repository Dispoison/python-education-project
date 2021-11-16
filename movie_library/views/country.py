from flask import request
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import Country, country_model
from movie_library.schema import CountrySchema
from movie_library.utils import admin_required, get_all_or_404, \
    add_model_object, update_model_object, delete_model_object


country_schema = CountrySchema()

country_ns = api.namespace(name='Country', path='/countries', description='country methods')


@country_ns.route('')
class CountriesResource(Resource):
    @country_ns.marshal_list_with(country_model)
    def get(self):
        return get_all_or_404(Country, 'No countries found.')

    @admin_required
    @country_ns.expect(country_model)
    @country_ns.marshal_with(country_model, code=201, description='The country was successfully created')
    def post(self):
        country = country_schema.load(request.json, session=db.session)
        return add_model_object(country)


@country_ns.route('/<int:country_id>')
class CountryResource(Resource):
    @country_ns.marshal_with(country_model)
    def get(self, country_id):
        return Country.query.get_or_404(country_id)

    @admin_required
    @country_ns.expect(country_model)
    @country_ns.marshal_with(country_model)
    def put(self, country_id):
        country = Country.query.get_or_404(country_id)
        country = country_schema.load(request.json, instance=country, session=db.session, partial=True)
        return update_model_object(country)

    @admin_required
    @country_ns.response(204, 'Successfully deleted')
    def delete(self, country_id):
        country = Country.query.get_or_404(country_id)
        return delete_model_object(country)
