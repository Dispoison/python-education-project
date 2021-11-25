"""Age restriction testing module"""

from http import HTTPStatus
import json
import pytest

from tests.utils import load_json


@pytest.fixture(scope='function')
def age_restrictions():
    """Fixture for preload age restriction objects"""
    return load_json('tests/age_restriction/age_restrictions.json')


class TestAgeRestrictionsUnauthorized:
    """Tests age restriction methods by unauthorized user"""

    @staticmethod
    def test_get_empty_table_404(client):
        """Tests get method on empty table by unauthorized user"""
        response = client.get('/age_restrictions')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /age_restrictions with empty table should return 404.'

    @staticmethod
    def test_get_by_id_empty_table_404(client):
        """Tests get by id method on empty table by unauthorized user"""
        response = client.get('/genres/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /genres/1 with empty table should return 404'

    @staticmethod
    def test_post_unauthorized_403(client, age_restrictions):
        """Tests post method by unauthorized user"""
        response = client.post('/age_restrictions', data=json.dumps(age_restrictions[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /age_restrictions by unauthorized should return 403'

    @staticmethod
    def test_put_unauthorized_403(client, age_restrictions):
        """Tests put method by unauthorized user"""
        response = client.put('/age_restrictions/1', data=json.dumps(age_restrictions[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /age_restrictions/1 by unauthorized should return 403'

    @staticmethod
    def test_delete_unauthorized_403(client):
        """Tests delete method by unauthorized user"""
        response = client.delete('/age_restrictions/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /age_restrictions/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestAgeRestrictionsUser:
    """Tests age restriction methods by authorized user"""

    @staticmethod
    def test_post_user_403(client, age_restrictions):
        """Tests post method by authorized user"""
        response = client.post('/age_restrictions', data=json.dumps(age_restrictions[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /age_restrictions by user should return 403'

    @staticmethod
    def test_put_authorized_403(client):
        """Tests put method by authorized user"""
        response = client.put('/age_restrictions/1', data=json.dumps({'title': '13+'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /age_restrictions/1 by user should return 403'

    @staticmethod
    def test_delete_authorized_403(client):
        """Tests delete method by authorized user"""
        response = client.delete('/age_restrictions/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /age_restrictions/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestAgeRestrictionsAdmin:
    """Tests age restriction methods by admin"""

    @staticmethod
    def test_post_admin_201(client, age_restrictions):
        """Tests post method by admin"""
        response = client.post('/age_restrictions', data=json.dumps(age_restrictions[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /age_restrictions by admin should return 201'

    @staticmethod
    @pytest.mark.parametrize('value', ['12+', '17+'])
    def test_put_admin_200(value, client):
        """Tests put method by admin"""
        response = client.put('/age_restrictions/1', data=json.dumps({'title': value}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /age_restrictions/1 by admin should return 200'
        assert response.json['title'] == value

    @staticmethod
    def test_delete_admin_204(client):
        """Tests delete method by admin"""
        response = client.delete('/age_restrictions/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /age_restrictions/1 by user should return 204'
