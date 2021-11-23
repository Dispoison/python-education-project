"""Director testing module"""

import pytest
import json
from http import HTTPStatus

from tests.utils import load_json


@pytest.fixture(scope='function')
def directors():
    return load_json('tests/director/directors.json')


class TestDirectorsUnauthorized:
    """Tests director methods by unauthorized user"""
    def test_get_empty_table_404(self, client):
        response = client.get('/directors')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /directors with empty table should return 404.'

    def test_get_by_id_empty_table_404(self, client):
        response = client.get('/directors/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /directors/1 with empty table should return 404'

    def test_post_unauthorized_403(self, client, directors):
        response = client.post('/directors', data=json.dumps(directors[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /directors by unauthorized should return 403'

    def test_put_unauthorized_403(self, client, directors):
        response = client.put('/directors/1', data=json.dumps(directors[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /directors/1 by unauthorized should return 403'

    def test_delete_unauthorized_403(self, client):
        response = client.delete('/directors/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /directors/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestDirectorsUser:
    """Tests director methods by authorized user"""
    def test_post_user_403(self, client, directors):
        response = client.post('/directors', data=json.dumps(directors[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /directors by user should return 403'

    def test_put_authorized_403(self, client):
        response = client.put('/directors/1', data=json.dumps({'first_name': 'Que'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /directors/1 by user should return 403'

    def test_delete_authorized_403(self, client):
        response = client.delete('/directors/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /directors/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestDirectorsAdmin:
    """Tests director methods by admin"""
    def test_post_admin_201(self, client, directors):
        response = client.post('/directors', data=json.dumps(directors[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /directors by admin should return 201'

    @pytest.mark.parametrize('first_name,last_name', [('John', 'Locke'),
                                                      ('Ivan', 'Ivanov')])
    def test_put_admin_200(self, client, first_name, last_name):
        response = client.put('/directors/1', data=json.dumps({'first_name': first_name,
                                                               'last_name': last_name}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /directors/1 by admin should return 200'
        assert response.json['first_name'] == first_name
        assert response.json['last_name'] == last_name

    def test_delete_admin_204(self, client):
        response = client.delete('/directors/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /directors/1 by user should return 204'
