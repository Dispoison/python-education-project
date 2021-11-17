"""Schemas module"""

from marshmallow_sqlalchemy import fields

from movie_library import ma
from movie_library.models import Movie, Director, Genre, Country, AgeRestriction, User


class DirectorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        load_instance = True


class GenreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True


class MovieSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Movie
        load_instance = True
        include_fk = True
        include_relationships = True
    genres = fields.Nested(GenreSchema, many=True)
    director = fields.Nested(DirectorSchema)


class CountrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        load_instance = True


class AgeRestrictionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AgeRestriction
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
