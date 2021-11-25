"""Country view module"""

from flask import request, abort
from flask_restx import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound

from movie_library import api, db
from movie_library.models import Country, country_model
from movie_library.schemes import CountrySchema
from movie_library.utils import admin_required, get_all_or_404, get_by_id_or_404, \
    add_model_object, update_model_object, delete_model_object, \
    log_error, log_info, log_object_info

country_schema = CountrySchema()

country_ns = api.namespace(name='Country', path='/countries', description='country methods')


@country_ns.route('')
class CountriesResource(Resource):
    """Country plural resource"""

    @country_ns.marshal_list_with(country_model)
    def get(self):
        """Returns list of country objects"""
        try:
            countries = get_all_or_404(Country)

            log_info()
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return countries

    @admin_required
    @country_ns.expect(country_model)
    @country_ns.marshal_with(country_model, code=201,
                             description='The country was successfully created')
    def post(self):
        """Creates country and returns deserialized object"""
        try:
            country = country_schema.load(request.json, session=db.session)

            add_model_object(country)

            log_object_info(country)
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return country, 201


@country_ns.route('/<int:country_id>')
class CountryResource(Resource):
    """Country singular resource"""

    @country_ns.marshal_with(country_model)
    def get(self, country_id: int):
        """Returns country object"""
        try:
            country = get_by_id_or_404(Country, country_id)

            log_info()
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return country

    @admin_required
    @country_ns.expect(country_model)
    @country_ns.marshal_with(country_model)
    def put(self, country_id: int):
        """Updates country and returns deserialized object"""
        try:
            country = get_by_id_or_404(Country, country_id)

            country = country_schema.load(request.json,
                                          instance=country,
                                          session=db.session,
                                          partial=True)

            update_model_object()

            log_object_info(country)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return country

    @admin_required
    @country_ns.response(204, 'Successfully deleted')
    def delete(self, country_id: int):
        """Deletes country object"""
        try:
            country = get_by_id_or_404(Country, country_id)

            delete_model_object(country)

            log_object_info(country)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return '', 204
