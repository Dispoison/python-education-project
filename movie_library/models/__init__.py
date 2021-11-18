"""Models package"""

from .movie_genre import movie_genre
from .director import Director, director_model, director_info_model
from .genre import Genre, genre_model
from .country import Country, country_model
from .age_restriction import AgeRestriction, age_restriction_model
from .user import User, login_model, register_model, user_info_model
from .movie import Movie, movie_model_deserialize, movie_model_serialize
