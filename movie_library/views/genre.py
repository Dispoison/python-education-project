from flask import jsonify, request, make_response
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import Genre
from movie_library.schema import GenreSchema
from movie_library.utils import jsonify_no_content

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@api.route('/genres')
class GenresResource(Resource):
    def get(self):
        genres = Genre.query.all()
        output = genres_schema.dump(genres)
        return jsonify(output)

    def post(self):
        genre = genre_schema.load(request.json, session=db.session)

        db.session.add(genre)
        db.session.commit()
        output = genre_schema.dump(genre)
        return make_response(jsonify(output), 201)


@api.route('/genre/<int:genre_id>')
class GenreResource(Resource):
    def get(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        output = genre_schema.dump(genre)
        return jsonify(output)

    def put(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        genre_updated = genre_schema.load(request.json, instance=genre, session=db.session)

        db.session.commit()
        output = genre_schema.dump(genre_updated)
        return jsonify(output)

    def delete(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        db.session.delete(genre)
        db.session.commit()
        return jsonify_no_content()
