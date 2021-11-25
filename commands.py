"""Commands module"""

from os import listdir, path
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

    @app.cli.command("create_tables")
    def create_tables():
        answer = input('Current tables will be dropped, are you sure? [yn]: ')
        if answer.lower() == 'y':
            db.drop_all()
            db.create_all()
            db.session.commit()
            print('Tables was successfully created.')

    @app.cli.command("insert_data")
    def insert_data():
        directory = 'db_insert_data'
        for file_name in sorted(listdir(directory)):
            with open(path.join(directory, file_name)) as table_inserts:
                print(f'Inserting data from {file_name}...')
                insert_commands = table_inserts.read().replace('\n', '')
                db.session.execute(insert_commands)
                print(f'Data from {file_name} was successfully inserted.')
        db.session.commit()
        print('All data was successfully inserted.')
