"""User testing module"""

from http import HTTPStatus
import json
import pytest

from tests.utils import load_json, register


@pytest.fixture(scope='function')
def users():
    """Fixture for preload user objects"""
    return load_json('tests/user/users.json')


class TestUser:
    """Tests register, logout and login"""

    @staticmethod
    def test_post_register(client, users):
        """Tests post method register"""
        response = client.post('/user/register', data=json.dumps(users[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /user/register should return 201'
        assert response.json['username'] == 'login'

    @staticmethod
    def test_post_logout(client):
        """Tests post method logout"""
        response = client.post('/user/logout')
        assert response.status_code == HTTPStatus.OK, \
            '[POST] /user/logout should return 200'
        assert response.json['message'] == 'Successfully logout.'

    @staticmethod
    def test_post_login(client):
        """Tests post method login"""
        response = client.post('/user/login', data=json.dumps({'username_or_email': 'login',
                                                               'password': 'password'}),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[POST] /user/login should return 200'
        assert response.json['message'] == 'Successfully authorized.'

    @staticmethod
    def test_post_password_change(client, users):
        """Tests post method password change"""
        register(client, users[0])
        response = client.post('/user/password-change',
                               data=json.dumps({'old_password': 'password',
                                                'new_password1': '12345',
                                                'new_password2': '12345'}),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[POST] /user/password-change should return 200'
