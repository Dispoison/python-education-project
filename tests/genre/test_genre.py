"""Genre testing module"""

from http import HTTPStatus
import json
import pytest

from tests.utils import load_json


@pytest.fixture(scope='function')
def genres():
    """Fixture for preload genre objects"""
    return load_json('tests/genre/genres.json')


class TestGenresUnauthorized:
    """Tests genre methods by unauthorized user"""

    @staticmethod
    def test_get_empty_table_404(client):
        """Tests get method on empty table by unauthorized user"""
        response = client.get('/genres')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /genres with empty table should return 404.'

    @staticmethod
    def test_get_by_id_empty_table_404(client):
        """Tests get by id method on empty table by unauthorized user"""
        response = client.get('/genres/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /genres/1 with empty table should return 404'

    @staticmethod
    def test_post_unauthorized_403(client, genres):
        """Tests post method by unauthorized user"""
        response = client.post('/genres', data=json.dumps(genres[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /genres by unauthorized should return 403'

    @staticmethod
    def test_put_unauthorized_403(client, genres):
        """Tests put method by unauthorized user"""
        response = client.put('/genres/1', data=json.dumps(genres[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /genres/1 by unauthorized should return 403'

    @staticmethod
    def test_delete_unauthorized_403(client):
        """Tests delete method by unauthorized user"""
        response = client.delete('/genres/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /genres/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestGenresUser:
    """Tests genre methods by authorized user"""

    @staticmethod
    def test_post_user_403(client, genres):
        """Tests post method by authorized user"""
        response = client.post('/genres', data=json.dumps(genres[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /genres by user should return 403'

    @staticmethod
    def test_put_authorized_403(client):
        """Tests put method by authorized user"""
        response = client.put('/genres/1', data=json.dumps({'title': 'Comedy'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /genres/1 by user should return 403'

    @staticmethod
    def test_delete_authorized_403(client):
        """Tests delete method by authorized user"""
        response = client.delete('/genres/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /genres/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestGenresAdmin:
    """Tests genre methods by admin"""

    @staticmethod
    def test_post_admin_201(client, genres):
        """Tests post method by admin"""
        response = client.post('/genres', data=json.dumps(genres[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /genres by admin should return 201'

    @staticmethod
    @pytest.mark.parametrize('value', ['Thriller', 'Drama'])
    def test_put_admin_200(value, client):
        """Tests put method by admin"""
        response = client.put('/genres/1', data=json.dumps({'title': value}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /genres/1 by admin should return 200'
        assert response.json['title'] == value

    @staticmethod
    def test_delete_admin_204(client):
        """Tests delete method by admin"""
        response = client.delete('/genres/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /genres/1 by user should return 204'
