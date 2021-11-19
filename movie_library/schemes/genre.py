"""Genre schema module"""

from marshmallow import fields, validates, ValidationError

from movie_library import ma
from movie_library.models import Genre


class GenreSchema(ma.SQLAlchemyAutoSchema):
    title = fields.String(required=True)

    class Meta:
        model = Genre
        load_instance = True

    @validates('title')
    def validate_title(self, title):
        if Genre.query.filter_by(title=title).first():
            raise ValidationError('The title value already exists.')
        if len(title) > 100:
            raise ValidationError('The title is longer than maximum length 100.')
        if len(title) <= 1:
            raise ValidationError('The title length must be longer than 1.')
