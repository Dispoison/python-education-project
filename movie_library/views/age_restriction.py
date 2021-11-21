"""Age restriction view module"""

from flask import request, abort
from flask_restx import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import NoResultFound

from movie_library import api, db
from movie_library.models import AgeRestriction, age_restriction_model
from movie_library.schemes import AgeRestrictionSchema
from movie_library.utils import admin_required, get_all_or_404, get_by_id_or_404, \
    add_model_object, update_model_object, delete_model_object, \
    log_error, log_info, log_object_info

age_restriction_schema = AgeRestrictionSchema()

age_restriction_ns = api.namespace(name='AgeRestriction', path='/age_restrictions',
                                   description='age restriction methods')


@age_restriction_ns.route('')
class AgeRestrictionsResource(Resource):
    """Age restriction plural resource"""

    @age_restriction_ns.marshal_list_with(age_restriction_model)
    def get(self):
        """Returns list of age restriction objects"""
        try:
            age_restrictions = get_all_or_404(AgeRestriction)

            log_info()
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return age_restrictions

    @admin_required
    @age_restriction_ns.expect(age_restriction_model)
    @age_restriction_ns.marshal_with(age_restriction_model, code=201,
                                     description='The age restriction was successfully created')
    def post(self):
        """Creates age restriction and returns deserialized object"""
        try:
            age_restriction = age_restriction_schema.load(request.json, session=db.session)

            add_model_object(age_restriction)

            log_object_info(age_restriction)
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return age_restriction, 201


@age_restriction_ns.route('/<int:age_restriction_id>')
class AgeRestrictionResource(Resource):
    """Age restriction singular resource"""

    @age_restriction_ns.marshal_with(age_restriction_model)
    def get(self, age_restriction_id: int):
        """Returns age restriction object"""
        try:
            age_restriction = get_by_id_or_404(AgeRestriction, age_restriction_id)

            log_info()
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return age_restriction

    @admin_required
    @age_restriction_ns.expect(age_restriction_model)
    @age_restriction_ns.marshal_with(age_restriction_model)
    def put(self, age_restriction_id: int):
        """Updates age restriction and returns deserialized object"""
        try:
            age_restriction = get_by_id_or_404(AgeRestriction, age_restriction_id)

            age_restriction = age_restriction_schema.load(request.json,
                                                          instance=age_restriction,
                                                          session=db.session,
                                                          partial=True)

            update_model_object()

            log_object_info(age_restriction)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return age_restriction

    @admin_required
    @age_restriction_ns.response(204, 'Successfully deleted')
    def delete(self, age_restriction_id: int):
        """Deletes age restriction object"""
        try:
            age_restriction = get_by_id_or_404(AgeRestriction, age_restriction_id)

            delete_model_object(age_restriction)

            log_object_info(age_restriction)
        except NoResultFound as error:
            log_error(error)
            return abort(404, str(error))
        else:
            return '', 204
