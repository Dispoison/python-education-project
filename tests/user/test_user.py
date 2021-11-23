"""User testing module"""

import pytest
import json
from http import HTTPStatus

from tests.utils import load_json


@pytest.fixture(scope='function')
def users():
    return load_json('tests/user/users.json')


class TestUser:
    """Tests register, logout and login"""
    def test_post_register(self, client, users):
        response = client.post('/user/register', data=json.dumps(users[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /user/register should return 201'
        assert response.json['username'] == 'login'

    def test_post_logout(self, client):
        response = client.post('/user/logout')
        assert response.status_code == HTTPStatus.OK, \
            '[POST] /user/logout should return 200'
        assert response.json['message'] == 'Successfully logout.'

    def test_post_login(self, client):
        response = client.post('/user/login', data=json.dumps({'username_or_email': 'login',
                                                               'password': 'password'}),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[POST] /user/login should return 200'
        assert response.json['message'] == 'Successfully authorized.'
