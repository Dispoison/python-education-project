import json

from tests.utils import load_json


class EntityLoader:
    @staticmethod
    def load_genres(client):
        genres = load_json('tests/genre/genres.json')
        for genre in genres:
            client.post('/genres', data=json.dumps(genre), content_type='application/json')

    @staticmethod
    def load_directors(client):
        directors = load_json('tests/director/directors.json')
        for director in directors:
            client.post('/directors', data=json.dumps(director), content_type='application/json')
