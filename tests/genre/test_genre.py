"""Genre testing module"""

import pytest
import json
from http import HTTPStatus

from tests.utils import load_json


@pytest.fixture(scope='function')
def genres():
    return load_json('tests/genre/genres.json')


class TestGenresUnauthorized:
    """Tests genre methods by unauthorized user"""
    def test_get_empty_table_404(self, client):
        response = client.get('/genres')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /genres with empty table should return 404.'

    def test_get_by_id_empty_table_404(self, client):
        response = client.get('/genres/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /genres/1 with empty table should return 404'

    def test_post_unauthorized_403(self, client, genres):
        response = client.post('/genres', data=json.dumps(genres[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /genres by unauthorized should return 403'

    def test_put_unauthorized_403(self, client, genres):
        response = client.put('/genres/1', data=json.dumps(genres[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /genres/1 by unauthorized should return 403'

    def test_delete_unauthorized_403(self, client):
        response = client.delete('/genres/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /genres/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestGenresUser:
    """Tests genre methods by authorized user"""
    def test_post_user_403(self, client, genres):
        response = client.post('/genres', data=json.dumps(genres[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /genres by user should return 403'

    def test_put_authorized_403(self, client):
        response = client.put('/genres/1', data=json.dumps({'title': 'Comedy'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /genres/1 by user should return 403'

    def test_delete_authorized_403(self, client):
        response = client.delete('/genres/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /genres/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestGenresAdmin:
    """Tests genre methods by admin"""
    def test_post_admin_201(self, client, genres):
        response = client.post('/genres', data=json.dumps(genres[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /genres by admin should return 201'

    @pytest.mark.parametrize('value', ['Thriller', 'Drama'])
    def test_put_admin_200(self, value, client):
        response = client.put('/genres/1', data=json.dumps({'title': value}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /genres/1 by admin should return 200'
        assert response.json['title'] == value

    def test_delete_admin_204(self, client):
        response = client.delete('/genres/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /genres/1 by user should return 204'
