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
            raise ValidationError('The title is longer than maximum length 50.')
        if len(first_name) <= 1:
            raise ValidationError('The title length must be longer than 1.')
        if first_name != first_name.capitalize():
            raise ValidationError('The title must be capitalized.')

    @validates('last_name')
    def validate_last_name(self, last_name):
        if len(last_name) > 50:
            raise ValidationError('The title is longer than maximum length 50.')
        if len(last_name) <= 1:
            raise ValidationError('The title length must be longer than 1.')
        if last_name != last_name.capitalize():
            raise ValidationError('The title must be capitalized.')
