"""Age restriction view module"""

from flask import request
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import AgeRestriction, age_restriction_model
from movie_library.schemes import AgeRestrictionSchema
from movie_library.utils import admin_required, get_all_or_404, \
    add_model_object, update_model_object, delete_model_object


age_restriction_schema = AgeRestrictionSchema()

age_restriction_ns = api.namespace(name='AgeRestriction', path='/age_restrictions',
                                   description='age restriction methods')


@age_restriction_ns.route('')
class AgeRestrictionsResource(Resource):
    """Age restriction plural resource"""
    @age_restriction_ns.marshal_list_with(age_restriction_model)
    def get(self):
        """Returns list of age restriction objects"""
        return get_all_or_404(AgeRestriction, 'No age restrictions found.')

    @admin_required
    @age_restriction_ns.expect(age_restriction_model)
    @age_restriction_ns.marshal_with(age_restriction_model, code=201,
                                     description='The age restriction was successfully created')
    def post(self):
        """Creates age restriction and returns deserialized object"""
        age_restriction = age_restriction_schema.load(request.json, session=db.session)
        return add_model_object(age_restriction)


@age_restriction_ns.route('/<int:age_restriction_id>')
class AgeRestrictionResource(Resource):
    """Age restriction singular resource"""
    @age_restriction_ns.marshal_with(age_restriction_model)
    def get(self, age_restriction_id: int):
        """Returns age restriction object"""
        return AgeRestriction.query.get_or_404(age_restriction_id)

    @admin_required
    @age_restriction_ns.expect(age_restriction_model)
    @age_restriction_ns.marshal_with(age_restriction_model)
    def put(self, age_restriction_id: int):
        """Updates age restriction and returns deserialized object"""
        age_restriction = AgeRestriction.query.get_or_404(age_restriction_id)
        age_restriction = age_restriction_schema.load(request.json,
                                                      instance=age_restriction, session=db.session)
        return update_model_object(age_restriction)

    @admin_required
    @age_restriction_ns.response(204, 'Successfully deleted')
    def delete(self, age_restriction_id: int):
        """Deletes age restriction object"""
        age_restriction = AgeRestriction.query.get_or_404(age_restriction_id)
        return delete_model_object(age_restriction)
