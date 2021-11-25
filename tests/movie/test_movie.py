"""Movie testing module"""

import json
import pytest
from http import HTTPStatus

from tests.utils import login_user, logout_user, load_json
from tests.movie.entity_loader import EntityLoader


@pytest.fixture(scope='function')
def movies():
    return load_json('tests/movie/movies.json')


@pytest.fixture(scope='class')
def load_background_entities(login_admin, client):
    EntityLoader.load_genres(client)
    EntityLoader.load_directors(client)


class TestMoviesUnauthorized:
    """Tests movie methods by unauthorized user"""
    def test_get_empty_table_404(self, client):
        response = client.get('/movies')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /movies with empty table should return 404.'

    def test_get_by_id_empty_table_404(self, client):
        response = client.get('/movies/1')
        assert response.status_code == HTTPStatus.NOT_FOUND, \
            '[GET] /movies/1 with empty table should return 404'

    def test_post_unauthorized_401(self, client, movies):
        response = client.post('/movies', data=json.dumps(movies[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            '[POST] /movies by unauthorized user should return 401'

    def test_put_unauthorized_401(self, client, movies):
        response = client.put('/movies/1', data=json.dumps(movies[0]),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            '[PUT] /movies/1 by unauthorized user should return 401'

    def test_delete_unauthorized_401(self, client):
        response = client.delete('/movies/1')
        assert response.status_code == HTTPStatus.UNAUTHORIZED, \
            '[PUT] /movies/1 by unauthorized user should return 401'


@pytest.mark.usefixtures('load_background_entities', 'login')
class TestMoviesAuthorized:
    """Tests movie methods by authorized user"""
    def test_post_authorized_201(self, client, movies):
        response = client.post('/movies', data=json.dumps(movies[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /movies by authorized user should return 201'
        assert response.json['title'] == 'The Dark Knight'

    def test_get_authorized_200(self, client):
        response = client.get('/movies')
        assert response.status_code == HTTPStatus.OK, \
            '[GET] /movies with not empty table should return 200.'
        assert response.json[0]['title'] == 'The Dark Knight'

    def test_get_by_id_authorized_200(self, client):
        response = client.get('/movies/1')
        assert response.status_code == HTTPStatus.OK, \
            '[GET] /movies/1 with not empty table should return 200'
        assert response.json['title'] == 'The Dark Knight'

    @pytest.mark.parametrize('value', ['Batman', 'The Dark Knight'])
    def test_put_authorized_200(self, value, client):
        response = client.put('/movies/1', data=json.dumps({'title': value}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.OK, \
            '[PUT] /movies/1 by authorized user should return 200'
        assert response.json['title'] == value

    def test_delete_authorized_204(self, client):
        response = client.delete('/movies/1')
        assert response.status_code == HTTPStatus.NO_CONTENT, \
            '[DELETE] /movies/1 by authorized user should return 204'


@pytest.mark.usefixtures('load_background_entities')
class TestMoviesDifferentUsers:
    """Tests movie post, put and delete methods by different user"""
    @pytest.fixture(scope='function')
    def login_first_user(self, client):
        login_user(client)
        yield
        logout_user(client)

    @pytest.fixture(scope='function')
    def login_another_user(self, client):
        login_user(client, login='another', password='12345')
        yield
        logout_user(client)

    def test_post_by_first_user_201(self, client, movies, login_first_user):
        response = client.post('/movies', data=json.dumps(movies[0]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /movies by first user should return 201'
        assert response.json['title'] == 'The Dark Knight'

    def test_put_by_another_user_403(self, client, login_another_user):
        response = client.put('/movies/1', data=json.dumps({'title': 'Batman'}),
                              content_type='application/json')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[PUT] /movies/1 by another user should return 403'

    def test_delete_by_another_user_403(self, client, login_another_user):
        response = client.delete('/movies/1')
        assert response.status_code == HTTPStatus.FORBIDDEN, \
            '[DELETE] /movies/1 by another user should return 204'


@pytest.mark.usefixtures('load_background_entities')
class TestMoviesQueryParameters:
    """Tests movie query parameters"""
    @pytest.mark.parametrize('movie_ind,value', [(0, 'The Dark Knight'),
                                                 (1, 'Terminator'),
                                                 (2, 'Forrest Gump'),
                                                 (3, 'Pulp Fiction')])
    def test_post_several_201(self, client, movies, movie_ind, value):
        response = client.post('/movies', data=json.dumps(movies[movie_ind]),
                               content_type='application/json')
        assert response.status_code == HTTPStatus.CREATED, \
            '[POST] /movies by authorized user should return 201'
        assert response.json['title'] == value

    def test_get(self, client):
        response = client.get('/movies')
        assert response.status_code == HTTPStatus.OK, \
            '[GET] /movies?q=ter should return 200 with one movie in dictionary'
        assert len(response.json) == 4

    def test_get_search(self, client):
        response = client.get('/movies?q=ter')
        assert response.status_code == HTTPStatus.OK, \
            '[GET] /movies?q=ter should return 200 with one movie in dictionary'
        assert response.json[0]['title'] == 'Terminator'
        assert len(response.json) == 1

    def test_get_pagination(self, client):
        response = client.get('/movies?page=3&page_size=1')
        assert response.status_code == HTTPStatus.OK, \
            '[GET] /movies?q=page=3&page_size=1 should return 200'
        assert response.json[0]['title'] == 'Forrest Gump'
        assert len(response.json) == 1

    @pytest.mark.parametrize('date_range,value', [('2000-01-01,', 'The Dark Knight'),
                                                  (',1985-01-01', 'Terminator'),
                                                  ('1980-01-01,1990-01-01', 'Terminator')])
    def test_get_release_date_range(self, client, date_range, value):
        response = client.get(f'/movies?release_date_range={date_range}')
        assert response.status_code == HTTPStatus.OK, \
            f'[GET] /movies?release_date_range={date_range} should return 200'
        assert response.json[0]['title'] == value
        assert len(response.json) == 1

    def test_get_sort(self, client):
        response = client.get('/movies?sort=rating;release_date,asc')
        assert response.status_code == HTTPStatus.OK, \
            '[GET] /movies?sort=rating;release_date,asc should return 200'
        assert response.json[0]['rating'] == 9.6
        assert response.json[1]['rating'] == 9.2
        assert response.json[1]['release_date'] == '1994-05-21T00:00:00'
        assert response.json[2]['rating'] == 9.2
        assert response.json[2]['release_date'] == '1994-06-24T00:00:00'
        assert response.json[3]['rating'] == 8.5
        assert len(response.json) == 4

    def test_get_by_directors(self, client):
        response = client.get('/movies?=directors=Quentin,stanley kub')
        assert response.json[0]['title'] == 'The Dark Knight'
        assert response.json[1]['title'] == 'Terminator'

    def test_get_by_genres(self, client):
        response = client.get('/movies?genres=Drama,crime')
        assert response.json[0]['title'] == 'Forrest Gump'
