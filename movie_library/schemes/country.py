"""Country schema module"""

from marshmallow import fields, validates, ValidationError

from movie_library import ma
from movie_library.models import Country


class CountrySchema(ma.SQLAlchemyAutoSchema):
    title = fields.String(required=True)
    abbreviation = fields.String(required=True)

    class Meta:
        model = Country
        load_instance = True

    @validates('title')
    def validate_title(self, title):
        if Country.query.filter_by(title=title).first():
            raise ValidationError('The title value already exists.')
        if len(title) > 100:
            raise ValidationError('The title is longer than maximum length 100.')
        if len(title) <= 1:
            raise ValidationError('The title length must be longer than 1.')
        if title[0] != title[0].upper():
            raise ValidationError('The first letter of title must be in upper case.')

    @validates('abbreviation')
    def validate_abbreviation(self, abbreviation):
        if Country.query.filter_by(abbreviation=abbreviation).first():
            raise ValidationError('The abbreviation value already exists.')
        if not abbreviation.isalpha():
            raise ValidationError('The abbreviation must consist only alphabetical characters.')
        if len(abbreviation) != 2:
            raise ValidationError('The abbreviation length must be 2.')
        if abbreviation != abbreviation.upper():
            raise ValidationError('The abbreviation must be in upper case.')
