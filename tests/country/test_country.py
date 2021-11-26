"""Country testing module"""

from http import HTTPStatus
import json
import pytest

from tests.utils import load_json


@pytest.fixture(scope='function')
def countries():
    """Fixture for preload country objects"""
    return load_json('tests/country/countries.json')


class TestCountriesUnauthorized:
    """Tests country methods by unauthorized user"""

    @staticmethod
    def test_get_empty_table_404(client):
        """Tests get method on empty table by unauthorized user"""
        response = client.get('/countries')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /countries with empty table should return 404.'

    @staticmethod
    def test_get_by_id_empty_table_404(client):
        """Tests get by id method on empty table by unauthorized user"""
        response = client.get('/countries/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /countries/1 with empty table should return 404'

    @staticmethod
    def test_post_unauthorized_403(client, countries):
        """Tests post method by unauthorized user"""
        response = client.post('/countries', data=json.dumps(countries[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /countries by unauthorized should return 403'

    @staticmethod
    def test_put_unauthorized_403(client, countries):
        """Tests put method by unauthorized user"""
        response = client.put('/countries/1', data=json.dumps(countries[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /countries/1 by unauthorized should return 403'

    @staticmethod
    def test_delete_unauthorized_403(client):
        """Tests delete method by unauthorized user"""
        response = client.delete('/countries/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /countries/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestCountriesUser:
    """Tests country methods by authorized user"""

    @staticmethod
    def test_post_user_403(client, countries):
        """Tests post method by authorized user"""
        response = client.post('/countries', data=json.dumps(countries[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /countries by user should return 403'

    @staticmethod
    def test_put_authorized_403(client):
        """Tests put method by authorized user"""
        response = client.put('/countries/1', data=json.dumps({'title': 'Turkey'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /countries/1 by user should return 403'

    @staticmethod
    def test_delete_authorized_403(client):
        """Tests delete method by authorized user"""
        response = client.delete('/countries/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /countries/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestCountriesAdmin:
    """Tests country methods by admin"""

    @staticmethod
    def test_post_admin_201(client, countries):
        """Tests post method by admin"""
        response = client.post('/countries', data=json.dumps(countries[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /countries by admin should return 201'

    @staticmethod
    @pytest.mark.parametrize('value', ['Turkey', 'Chad'])
    def test_put_admin_200(value, client):
        """Tests put method by admin"""
        response = client.put('/countries/1', data=json.dumps({'title': value}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /countries/1 by admin should return 200'
        assert response.json['title'] == value

    @staticmethod
    def test_delete_admin_204(client):
        """Tests delete method by admin"""
        response = client.delete('/countries/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /countries/1 by user should return 204'
