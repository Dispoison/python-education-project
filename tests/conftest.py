import pytest

from movie_library import create_app, db
from tests.utils import create_superuser, create_user, create_another_user, login_user, logout_user


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    yield app


@pytest.fixture(scope='class', autouse=True)
def client(app):
    with app.app_context():
        db.create_all()
        create_superuser(db)
        create_user(db)
        create_another_user(db)
        with app.test_client() as client:
            yield client

    db.session.remove()
    db.drop_all(app=app)


@pytest.fixture(scope='class')
def login(client):
    login_user(client)
    yield
    logout_user(client)


@pytest.fixture(scope='class')
def login_admin(client):
    login_user(client, login='admin', password='admin')
    yield
    logout_user(client)
