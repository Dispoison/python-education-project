from flask import jsonify, request, make_response
from flask_restx import Resource

from movie_library import api, db
from movie_library.models import Director
from movie_library.schema import DirectorSchema
from movie_library.utils import jsonify_no_content

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@api.route('/directors')
class DirectorsResource(Resource):
    def get(self):
        directors = Director.query.all()
        output = directors_schema.dump(directors)
        return jsonify(output)

    def post(self):
        director = director_schema.load(request.json, session=db.session)

        db.session.add(director)
        db.session.commit()
        output = director_schema.dump(director)
        return make_response(jsonify(output), 201)


@api.route('/director/<int:director_id>')
class DirectorResource(Resource):
    def get(self, director_id):
        director = Director.query.get_or_404(director_id)
        output = director_schema.dump(director)
        return jsonify(output)

    def put(self, director_id):
        director = Director.query.get_or_404(director_id)
        director_updated = director_schema.load(request.json, instance=director, session=db.session)

        db.session.commit()
        output = director_schema.dump(director_updated)
        return jsonify(output)

    def delete(self, director_id):
        director = Director.query.get_or_404(director_id)
        db.session.delete(director)
        db.session.commit()
        return jsonify_no_content()
