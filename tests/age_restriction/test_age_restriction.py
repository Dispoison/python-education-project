"""Age restriction testing module"""

import pytest
import json
from http import HTTPStatus

from tests.utils import load_json


@pytest.fixture(scope='function')
def age_restrictions():
    return load_json('tests/age_restriction/age_restrictions.json')


class TestAgeRestrictionsUnauthorized:
    """Tests age restriction methods by unauthorized user"""
    def test_get_empty_table_404(self, client):
        response = client.get('/age_restrictions')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /age_restrictions with empty table should return 404.'

    def test_get_by_id_empty_table_404(self, client):
        response = client.get('/genres/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /genres/1 with empty table should return 404'

    def test_post_unauthorized_403(self, client, age_restrictions):
        response = client.post('/age_restrictions', data=json.dumps(age_restrictions[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /age_restrictions by unauthorized should return 403'

    def test_put_unauthorized_403(self, client, age_restrictions):
        response = client.put('/age_restrictions/1', data=json.dumps(age_restrictions[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /age_restrictions/1 by unauthorized should return 403'

    def test_delete_unauthorized_403(self, client):
        response = client.delete('/age_restrictions/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /age_restrictions/1 by unauthorized should return 403'


@pytest.mark.usefixtures('login')
class TestAgeRestrictionsUser:
    """Tests age restriction methods by authorized user"""
    def test_post_user_403(self, client, age_restrictions):
        response = client.post('/age_restrictions', data=json.dumps(age_restrictions[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[POST] /age_restrictions by user should return 403'

    def test_put_authorized_403(self, client):
        response = client.put('/age_restrictions/1', data=json.dumps({'title': '13+'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /age_restrictions/1 by user should return 403'

    def test_delete_authorized_403(self, client):
        response = client.delete('/age_restrictions/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /age_restrictions/1 by user should return 403'


@pytest.mark.usefixtures('login_admin')
class TestAgeRestrictionsAdmin:
    """Tests age restriction methods by admin"""
    def test_post_admin_201(self, client, age_restrictions):
        response = client.post('/age_restrictions', data=json.dumps(age_restrictions[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /age_restrictions by admin should return 201'

    @pytest.mark.parametrize('value', ['12+', '17+'])
    def test_put_admin_200(self, value, client):
        response = client.put('/age_restrictions/1', data=json.dumps({'title': value}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /age_restrictions/1 by admin should return 200'
        assert response.json['title'] == value

    def test_delete_admin_204(self, client):
        response = client.delete('/age_restrictions/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /age_restrictions/1 by user should return 204'
