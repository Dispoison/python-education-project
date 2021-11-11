from flask import jsonify, request, make_response
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import Movie, Genre
from movie_library.schema import MovieSchema
from movie_library.utils import jsonify_no_content

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@api.route('/movies')
class MoviesResource(Resource):
    def get(self):
        movies = Movie.query.all()
        output = movies_schema.dump(movies)
        return jsonify(output)

    def post(self):
        genres_ids = request.json.get('genres', [])
        if 'genres' in request.json:
            del request.json['genres']
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
        return jsonify(output)

    def put(self, movie_id):
        genres_ids = request.json.get('genres', [])
        if 'genres' in request.json:
            del request.json['genres']
        movie = Movie.query.get_or_404(movie_id)
        movie_updated = movie_schema.load(request.json, instance=movie, session=db.session)
        genres = Genre.query.filter(Genre.id.in_(genres_ids)).all()

        movie.genres = genres
        db.session.commit()
        output = movie_schema.dump(movie_updated)
        return jsonify(output)

    def delete(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return jsonify_no_content()