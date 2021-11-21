"""Commands module"""

from re import match
from getpass import getpass

from flask import Flask
from marshmallow.exceptions import ValidationError
from werkzeug.security import generate_password_hash

from movie_library import db
from movie_library.models import User
from movie_library.schemes.user import RegisterSchema


def add_commands(app: Flask):
    """Adds commands to application"""
    @app.cli.command('createsuperuser')
    def create_superuser():
        """Creates admin in cli"""
        try:
            register_schema = RegisterSchema()

            username = input('Username: ')
            register_schema.validate_username(username)

            email = input('Email: ')
            if not match(r'^[A-Za-z0-9]+[._]?[A-Za-z0-9]+[@][A-Za-z]+[.][a-z]{2,3}$', email):
                raise ValidationError('The email has the wrong format')
            register_schema.validate_username(email)

            password1 = getpass('Password: ')
            password2 = getpass('Password (again): ')
            register_schema.validate_passwords(password1, password2)

            hash_pwd = generate_password_hash(password1)

            admin = User(username=username, email=email, password=hash_pwd, is_admin=True)

            db.session.add(admin)
            db.session.commit()

            print(f'{repr(admin)} successfully created')
        except ValidationError as error:
            print(str(error))
