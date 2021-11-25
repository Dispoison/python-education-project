"""Director schema module"""

from marshmallow import fields, validates, ValidationError

from movie_library import ma
from movie_library.models import Director


class DirectorSchema(ma.SQLAlchemyAutoSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    description = fields.String()

    class Meta:
        model = Director
        load_instance = True

    @validates('first_name')
    def validate_first_name(self, first_name):
        if len(first_name) > 50:
            raise ValidationError('The first name is longer than maximum length 50.')
        if len(first_name) <= 1:
            raise ValidationError('The first name length must be longer than 1.')
        if first_name[0] != first_name[0].upper():
            raise ValidationError('The first letter of first name must be in upper case.')

    @validates('last_name')
    def validate_last_name(self, last_name):
        if len(last_name) > 50:
            raise ValidationError('The last name is longer than maximum length 50.')
        if len(last_name) <= 1:
            raise ValidationError('The last name length must be longer than 1.')
        if last_name[0] != last_name[0].upper():
            raise ValidationError('The first letter of last name  must be in upper case.')
