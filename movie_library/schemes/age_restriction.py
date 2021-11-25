"""Age restriction schema module"""

from re import match

from marshmallow import fields, validates, ValidationError

from movie_library import ma
from movie_library.models import AgeRestriction


class AgeRestrictionSchema(ma.SQLAlchemyAutoSchema):
    title = fields.String(required=True)

    class Meta:
        model = AgeRestriction
        load_instance = True

    @validates('title')
    def validate_title(self, title):
        if AgeRestriction.query.filter_by(title=title).first():
            raise ValidationError('The title value already exists.')
        if len(title) > 3:
            raise ValidationError('The title is longer than maximum length 3.')
        if len(title) <= 1:
            raise ValidationError('The title length must be longer than 1.')
        if not match(r'^\d{1,2}\+$', title):
            raise ValidationError('The title must match pattern \'number+\'')
