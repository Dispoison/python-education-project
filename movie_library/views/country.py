from flask import jsonify, request, make_response
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import Country
from movie_library.schema import CountrySchema
from movie_library.utils import jsonify_no_content

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)


@api.route('/countries')
class CountriesResource(Resource):
    def get(self):
        countries = Country.query.all()
        output = countries_schema.dump(countries)
        return jsonify(output)

    def post(self):
        country = country_schema.load(request.json, session=db.session)

        db.session.add(country)
        db.session.commit()
        output = country_schema.dump(country)
        return make_response(jsonify(output), 201)


@api.route('/country/<int:country_id>')
class CountryResource(Resource):
    def get(self, country_id):
        country = Country.query.get_or_404(country_id)
        output = country_schema.dump(country)
        return jsonify(output)

    def put(self, country_id):
        country = Country.query.get_or_404(country_id)
        country_updated = country_schema.load(request.json, instance=country, session=db.session)

        db.session.commit()
        output = country_schema.dump(country_updated)
        return jsonify(output)

    def delete(self, country_id):
        country = Country.query.get_or_404(country_id)
        db.session.delete(country)
        db.session.commit()
        return jsonify_no_content()
