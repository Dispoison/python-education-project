from flask import jsonify, request, make_response
from flask_restx import Resource
from flask_login import login_required, current_user
from sqlalchemy.exc import NoResultFound

from movie_library import api, db
from movie_library.models import Movie, Genre
from movie_library.schema import MovieSchema
from movie_library.utils import jsonify_no_content, populate_default_if_none

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@api.route('/movies')
class MoviesResource(Resource):
    def get(self):
        try:
            search_data = request.args.get('q', '')
            sort_data = request.args.getlist('sort')
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 10))
            release_date_range = request.args.get('release_date_range', ',')
            directors = request.args.get('directors', '').split(',')
            genres = request.args.get('genres', ',').split(',')

            movies = Movie.get_movies_by(search_data, sort_data, page, page_size, release_date_range, directors, genres)
        except ValueError as value_error:
            return make_response({'message': str(value_error)}, 400)
        except NoResultFound as not_found:
            return make_response({'message': str(not_found)}, 404)

        output = movies_schema.dump(movies)
        for movie in output:
            populate_default_if_none(movie, 'director', 'unknown')
        return jsonify(output)

    @login_required
    def post(self):
        genres_ids = request.json.get('genres', [])
        if 'genres' in request.json:
            del request.json['genres']
        request.json['user_id'] = current_user.get_id()
        movie = movie_schema.load(request.json, session=db.session)
        genres = Genre.query.filter(Genre.id.in_(genres_ids)).all()

        movie.genres = genres
        db.session.add(movie)
        db.session.commit()
        output = movie_schema.dump(movie)
        return make_response(jsonify(output), 201)


@api.route('/movie/<int:movie_id>')
class MovieResource(Resource):
    def get(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        output = movie_schema.dump(movie)
        populate_default_if_none(output, 'director', 'unknown')
        return jsonify(output)

    @login_required
    def put(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        if not (current_user.is_admin or current_user.id == movie.user_id):
            return make_response({'message': 'A movie can only be edited by the user who added it '
                                             'or by the administrator.'}, 403)
        genres_ids = request.json.get('genres', [])
        if 'genres' in request.json:
            del request.json['genres']
        movie_updated = movie_schema.load(request.json, instance=movie, session=db.session)
        genres = Genre.query.filter(Genre.id.in_(genres_ids)).all()

        movie.genres = genres
        db.session.commit()
        output = movie_schema.dump(movie_updated)
        return jsonify(output)

    @login_required
    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        if not (current_user.is_admin or current_user.id == movie.user_id):
            return make_response({'message': 'A movie can only be deleted by the user who added it '
                                             'or by the administrator.'}, 403)
        db.session.delete(movie)
        db.session.commit()
        return jsonify_no_content()
