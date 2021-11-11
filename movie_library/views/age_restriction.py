from flask import jsonify, request, make_response
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import AgeRestriction
from movie_library.schema import AgeRestrictionSchema
from movie_library.utils import jsonify_no_content

age_restriction_schema = AgeRestrictionSchema()
age_restrictions_schema = AgeRestrictionSchema(many=True)


@api.route('/age_restrictions')
class AgeRestrictionsResource(Resource):
    def get(self):
        age_restrictions = AgeRestriction.query.all()
        output = age_restrictions_schema.dump(age_restrictions)
        return jsonify(output)

    def post(self):
        age_restriction = age_restriction_schema.load(request.json, session=db.session)

        db.session.add(age_restriction)
        db.session.commit()
        output = age_restriction_schema.dump(age_restriction)
        return make_response(jsonify(output), 201)


@api.route('/age_restriction/<int:age_restriction_id>')
class AgeRestrictionResource(Resource):
    def get(self, age_restriction_id):
        age_restriction = AgeRestriction.query.get_or_404(age_restriction_id)
        output = age_restriction_schema.dump(age_restriction)
        return jsonify(output)

    def put(self, age_restriction_id):
        age_restriction = AgeRestriction.query.get_or_404(age_restriction_id)
        age_restriction_updated = age_restriction_schema.load(request.json,
                                                              instance=age_restriction, session=db.session)

        db.session.commit()
        output = age_restriction_schema.dump(age_restriction_updated)
        return jsonify(output)

    def delete(self, age_restriction_id):
        age_restriction = AgeRestriction.query.get_or_404(age_restriction_id)
        db.session.delete(age_restriction)
        db.session.commit()
        return jsonify_no_content()
