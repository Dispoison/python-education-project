from datetime import datetime
from typing import List

from sqlalchemy import func, or_
from sqlalchemy.exc import NoResultFound

from movie_library import db
from movie_library.models import movie_genre, Director, Genre
from movie_library.utils import get_order_objects_list

VALID_SORTING_VALUES = ('rating', 'release_date')
MIN_DATE = datetime.min
MAX_DATE = datetime.max


class Movie(db.Model):
    """Contains the properties and relationships of the movie"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Numeric(4, 2))
    description = db.Column(db.Text)
    preview = db.Column(db.String(100))
    budget = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    age_restriction_id = db.Column(db.Integer, db.ForeignKey('age_restriction.id'))
    genres = db.relationship('Genre', secondary=movie_genre,
                             backref=db.backref('movies'), lazy=True)

    def __repr__(self):
        return f'<Movie {self.title}>'

    @classmethod
    def get_movies_by(cls, search_data: str, sort_data: List[str], page: int, page_size: int,
                      release_date_range: str, directors: List[str], genres: List[str]) -> list:
        """Returns searched, paginated, sorted and filtered movies"""
        offset = page_size * (page - 1)

        order_by = get_order_objects_list(sort_data, cls, VALID_SORTING_VALUES)

        date_range = release_date_range.split(',')
        date_range[0] = MIN_DATE if date_range[0] == '' else datetime.strptime(date_range[0], '%Y-%m-%d')
        date_range[1] = MAX_DATE if date_range[1] == '' else datetime.strptime(date_range[1], '%Y-%m-%d')

        directors_conditions = [func.concat(Director.first_name, ' ', Director.last_name).ilike(f'%{director}%')
                                for director in directors]

        genres_conditions = or_(*[Genre.title.ilike(f'%{genre}%') for genre in genres])

        movies = cls.query. \
            order_by(*order_by). \
            filter(cls.title.ilike(f'%{search_data}%')). \
            filter(Movie.release_date.between(*date_range)). \
            join(Movie.director).filter(or_(*directors_conditions)). \
            join(movie_genre, Movie.id == movie_genre.c.movie_id).join(Genre, movie_genre.c.genre_id == Genre.id). \
            filter(genres_conditions). \
            group_by(Movie.id).having(db.func.every(db.exists().
                                                    where(db.and_(movie_genre.c.genre_id == Genre.id,
                                                                  movie_genre.c.movie_id == Movie.id)).
                                                    correlate_except(movie_genre))). \
            offset(offset).limit(page_size).all()

        if not movies:
            raise NoResultFound('No movies found.')

        return movies
