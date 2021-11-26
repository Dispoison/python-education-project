"""Utils module for tests"""

import json
from werkzeug.security import generate_password_hash

from movie_library.models.user import User


def load_json(file_path: str) -> list:
    """Loads json from file"""
    with open(file_path, encoding='utf8') as file:
        object_list = json.load(file)
    return object_list


def create_superuser(db):
    """Creates admin"""
    admin = User(username='admin', email='admin@mail.com',
                 password=generate_password_hash('admin'), is_admin=True)
    db.session.add(admin)
    db.session.commit()


def create_user(db):
    """Creates user"""
    user = User(username='username', email='email@mail.com',
                password=generate_password_hash('12345'))
    db.session.add(user)
    db.session.commit()


def create_another_user(db):
    """Creates another user"""
    another_user = User(username='another', email='another@mail.com',
                        password=generate_password_hash('12345'))
    db.session.add(another_user)
    db.session.commit()


def register(client, user_dict):
    """Register user"""
    client.post('/user/register', data=json.dumps(user_dict),
                content_type='application/json')


def logout_user(client):
    """Log out user"""
    client.post('/user/logout')


def login_user(client, login='username', password='12345'):
    """Log in user"""
    client.post('/user/login', data=json.dumps(
        {"username_or_email": login, "password": password}),
                content_type="application/json")
