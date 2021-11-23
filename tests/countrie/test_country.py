"""Country testing module"""

import pytest
import json
from http import HTTPStatus

from tests.utils import load_json


@pytest.fixture(scope='function')
def countries():
    return load_json('tests/countrie/countries.json')


class TestCountriesUnauthorized:
    """Tests country methods by unauthorized user"""
    def test_get_empty_table_404(self, client):
        response = client.get('/countries')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /countries with empty table should return 404.'

    def test_get_by_id_empty_table_404(self, client):
        response = client.get('/countries/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /countries/1 with empty table should return 404'

    def test_post_unauthorized_403(self, client, countries):
        response = client.post('/countries', data=json.dumps(countries[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /countries by unauthorized should return 403'

    def test_put_unauthorized_403(self, client, countries):
        response = client.put('/countries/1', data=json.dumps(countries[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /countries/1 by unauthorized should return 403'

    def test_delete_unauthorized_403(self, client):
        response = client.delete('/countries/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /countries/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestCountriesUser:
    """Tests country methods by authorized user"""
    def test_post_user_403(self, client, countries):
        response = client.post('/countries', data=json.dumps(countries[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /countries by user should return 403'

    def test_put_authorized_403(self, client):
        response = client.put('/countries/1', data=json.dumps({'title': 'Turkey'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /countries/1 by user should return 403'

    def test_delete_authorized_403(self, client):
        response = client.delete('/countries/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /countries/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestCountriesAdmin:
    """Tests country methods by admin"""
    def test_post_admin_201(self, client, countries):
        response = client.post('/countries', data=json.dumps(countries[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /countries by admin should return 201'

    @pytest.mark.parametrize('value', ['Turkey', 'Chad'])
    def test_put_admin_200(self, value, client):
        response = client.put('/countries/1', data=json.dumps({'title': value}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /countries/1 by admin should return 200'
        assert response.json['title'] == value

    def test_delete_admin_204(self, client):
        response = client.delete('/countries/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /countries/1 by user should return 204'
