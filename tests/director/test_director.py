"""Director testing module"""

from http import HTTPStatus
import json
import pytest

from tests.utils import load_json


@pytest.fixture(scope='function')
def directors():
    """Fixture for preload director objects"""
    return load_json('tests/director/directors.json')


class TestDirectorsUnauthorized:
    """Tests director methods by unauthorized user"""

    @staticmethod
    def test_get_empty_table_404(client):
        """Tests get method on empty table by unauthorized user"""
        response = client.get('/directors')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /directors with empty table should return 404.'

    @staticmethod
    def test_get_by_id_empty_table_404(client):
        """Tests get by id method on empty table by unauthorized user"""
        response = client.get('/directors/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /directors/1 with empty table should return 404'

    @staticmethod
    def test_post_unauthorized_403(client, directors):
        """Tests post method by unauthorized user"""
        response = client.post('/directors', data=json.dumps(directors[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /directors by unauthorized should return 403'

    @staticmethod
    def test_put_unauthorized_403(client, directors):
        """Tests put method by unauthorized user"""
        response = client.put('/directors/1', data=json.dumps(directors[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /directors/1 by unauthorized should return 403'

    @staticmethod
    def test_delete_unauthorized_403(client):
        """Tests delete method by unauthorized user"""
        response = client.delete('/directors/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /directors/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestDirectorsUser:
    """Tests director methods by authorized user"""

    @staticmethod
    def test_post_user_403(client, directors):
        """Tests post method by authorized user"""
        response = client.post('/directors', data=json.dumps(directors[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /directors by user should return 403'

    @staticmethod
    def test_put_authorized_403(client):
        """Tests put method by authorized user"""
        response = client.put('/directors/1', data=json.dumps({'first_name': 'Que'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /directors/1 by user should return 403'

    @staticmethod
    def test_delete_authorized_403(client):
        """Tests delete method by authorized user"""
        response = client.delete('/directors/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /directors/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestDirectorsAdmin:
    """Tests director methods by admin"""

    @staticmethod
    def test_post_admin_201(client, directors):
        """Tests post method by admin"""
        response = client.post('/directors', data=json.dumps(directors[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /directors by admin should return 201'

    @staticmethod
    @pytest.mark.parametrize('first_name,last_name', [('John', 'Locke'),
                                                      ('Ivan', 'Ivanov')])
    def test_put_admin_200(client, first_name, last_name):
        """Tests put method by admin"""
        response = client.put('/directors/1', data=json.dumps({'first_name': first_name,
                                                               'last_name': last_name}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /directors/1 by admin should return 200'
        assert response.json['first_name'] == first_name
        assert response.json['last_name'] == last_name

    @staticmethod
    def test_delete_admin_204(client):
        """Tests delete method by admin"""
        response = client.delete('/directors/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /directors/1 by user should return 204'
