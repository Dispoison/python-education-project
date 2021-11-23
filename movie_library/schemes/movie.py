"""Movie schema module"""

from typing import List

from marshmallow import fields, validates, ValidationError

from movie_library import ma
from movie_library.models import Movie, Genre


class MovieSchema(ma.SQLAlchemyAutoSchema):
    title = fields.String(required=True)
    release_date = fields.DateTime(required=True)
    duration = fields.Integer(required=True)
    rating = fields.Decimal(places=2)
    description = fields.String()
    preview = fields.String()
    budget = fields.Float()
    director_id = fields.Integer()
    country_id = fields.Integer()
    age_restriction_id = fields.Integer()
    genres = fields.List(fields.Integer)

    class Meta:
        model = Movie
        load_instance = True
        include_fk = True

    @validates('title')
    def validate_title(self, title):
        if len(title) > 255:
            raise ValidationError('The title is longer than maximum length 255.')
        if len(title) <= 1:
            raise ValidationError('The title length must be longer than 1.')

    @validates('duration')
    def validate_duration(self, duration):
        if duration < 0:
            raise ValidationError('The duration must be positive.')

    @validates('rating')
    def validate_rating(self, rating):
        if not (0 <= rating <= 10):
            raise ValidationError('The rating must be in range from 0 to 10.')

    @validates('preview')
    def validate_preview(self, preview):
        if len(preview) > 255:
            raise ValidationError('The preview is longer than maximum length 255.')

    @validates('budget')
    def validate_budget(self, budget):
        if budget < 0:
            raise ValidationError('The duration must be positive.')

    @staticmethod
    def validate_id(object_id, var_name):
        if object_id < 1:
            raise ValidationError(f'The {var_name} must be bigger than 0.')

    @validates('user_id')
    def validate_user_id(self, user_id):
        MovieSchema.validate_id(user_id, 'user_id')

    @validates('director_id')
    def validate_director_id(self, director_id):
        MovieSchema.validate_id(director_id, 'director_id')

    @validates('country_id')
    def validate_country_id(self, country_id):
        MovieSchema.validate_id(country_id, 'country_id')

    @validates('age_restriction_id')
    def validate_age_restriction_id(self, age_restriction_id):
        MovieSchema.validate_id(age_restriction_id, 'age_restriction_id')

    @staticmethod
    def validate_genres_ids(genres_ids: List[int]):
        if (not isinstance(genres_ids, list) or not all(isinstance(id_, int) for id_ in genres_ids)) and \
                genres_ids is not None:
            raise ValidationError({'genres': ['Genres must be a list of integers.']})
        for genre_id in genres_ids:
            if not Genre.query.get(genre_id):
                raise ValidationError({'genres': [f'Genre index {genre_id} does not exist.']})
