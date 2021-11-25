"""User schema module"""

from marshmallow import fields, pre_load, validates, ValidationError, EXCLUDE
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from movie_library import ma
from movie_library.models import User
from movie_library.utils import AuthenticationError


class LoginSchema(ma.SQLAlchemyAutoSchema):
    @staticmethod
    def validate_user_login(username_or_email, password):
        if not username_or_email:
            raise ValidationError({'username_or_email': ['The username_or_email is missing']})
        if not password:
            raise ValidationError({'password': ['The password field is missing']})

    @staticmethod
    def authenticate_user(username_or_email, password):
        user = User.query.filter(or_(User.username == username_or_email,
                                     User.email == username_or_email)).first()

        if not (user and check_password_hash(user.password, password)):
            raise AuthenticationError('Login or password are incorrect.')
        return user


class RegisterSchema(ma.SQLAlchemyAutoSchema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    first_name = fields.String()
    last_name = fields.String()

    class Meta:
        model = User
        load_instance = True
        exclude = 'is_admin',
        unknown = EXCLUDE

    @pre_load()
    def pre_load_schema(self, in_data, **kwargs):
        self.validate_passwords(in_data.get('password1'), in_data.get('password2'))
        in_data['password'] = generate_password_hash(in_data.get('password1'))
        return in_data

    @staticmethod
    def validate_passwords(password1, password2):
        if not password1:
            raise ValidationError({'password1': ['The password1 is missing']})
        if not password2:
            raise ValidationError({'password2': ['The password2 is missing']})
        if password1 != password2:
            raise ValidationError({'password2': ['Passwords are not equal.']})
        if not (5 <= len(password1) <= 24):
            raise ValidationError({'password1': ['The password length must be in range from 5 to 24.']})
        if not password1.isalnum():
            raise ValidationError({'password1': ['The password must be alphanumeric.']})

    @validates('username')
    def validate_username(self, username):
        if User.query.filter_by(username=username).first():
            raise ValidationError('The username value already exists.')
        if len(username) > 150:
            raise ValidationError('The username is longer than maximum length 150.')
        if len(username) <= 3:
            raise ValidationError('The username length must be longer than 3.')

    @validates('email')
    def validate_email(self, email):
        if User.query.filter_by(email=email).first():
            raise ValidationError('The email value already exists.')
        if len(email) > 150:
            raise ValidationError('The email is longer than maximum length 150.')
        if len(email) <= 6:
            raise ValidationError('The email length must be longer than 6.')

    @validates('first_name')
    def validate_first_name(self, first_name):
        if len(first_name) > 50:
            raise ValidationError('The first_name is longer than maximum length 50.')
        if len(first_name) <= 1:
            raise ValidationError('The first_name length must be longer than 1.')

    @validates('last_name')
    def validate_last_name(self, last_name):
        if len(last_name) > 50:
            raise ValidationError('The last_name is longer than maximum length 50.')
        if len(last_name) <= 1:
            raise ValidationError('The last_name length must be longer than 1.')
