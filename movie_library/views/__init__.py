"""Views package"""

from .movie import MoviesResource, MovieResource
from .director import DirectorsResource, DirectorResource
from .genre import GenresResource, GenreResource
from .country import CountriesResource, CountryResource
from .age_restriction import AgeRestrictionsResource, AgeRestrictionResource
from .user import UserLogin, UserLogout, UserRegister
