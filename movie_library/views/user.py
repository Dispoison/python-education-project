"""User view module"""

from datetime import datetime

from flask import request, make_response, abort, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flask_restx import Resource
from marshmallow.exceptions import ValidationError
from werkzeug.security import generate_password_hash

from movie_library import api, db
from movie_library.models import login_model, register_model, \
    user_info_model, password_change_model, User
from movie_library.schemes import LoginSchema, RegisterSchema, PasswordChangeSchema
from movie_library.utils import AuthenticationError, add_model_object, \
    unauthorized_required, refresh_and_login_user, log_error, log_info, update_model_object

login_schema = LoginSchema()
register_schema = RegisterSchema()
password_change_schema = PasswordChangeSchema()


user_ns = api.namespace(name='User', path='/user', description='user methods')


@user_ns.route('/login')
class UserLogin(Resource):
    """User login resource"""

    @staticmethod
    @unauthorized_required
    @user_ns.expect(login_model)
    def post():
        """Provides user authentication"""
        try:
            login = request.json.get('username_or_email')
            password = request.json.get('password')
            login_schema.validate_user_login(login, password)
            user = login_schema.authenticate_user(login, password)
            refresh_and_login_user(user)

            log_info()
        except ValidationError as error:
            log_error(error)
            return abort(400, error.messages)
        except AuthenticationError as error:
            log_error(error)
            return abort(401, str(error))
        else:
            return make_response({'message': 'Successfully authorized.'}, 200)


@user_ns.route('/logout')
class UserLogout(Resource):
    """User logout resource"""

    @staticmethod
    @login_required
    def post():
        """Provides user logout"""
        log_info()
        logout_user()
        return make_response({'message': 'Successfully logout.'}, 200)


@user_ns.route('/password-change')
class UserPasswordChange(Resource):
    """User password changing"""

    @staticmethod
    @login_required
    @user_ns.expect(password_change_model)
    def post():
        """Provides user password change"""
        try:
            old_password = request.json.get('old_password')
            new_password1 = request.json.get('new_password1')
            new_password2 = request.json.get('new_password2')

            password_change_schema.verify_password_with_current(old_password)
            password_change_schema.validate_new_passwords(new_password1, new_password2)

            user = User.query.filter_by(username=current_user.username).first()

            hash_pwd = generate_password_hash(new_password1)
            user.password = hash_pwd

            update_model_object()

            log_info()
        except ValidationError as error:
            log_error(error)
            return abort(400, error.messages)
        except AuthenticationError as error:
            log_error(error)
            return abort(401, str(error))
        else:
            return make_response({'message': 'Password successfully changed.'}, 200)


@user_ns.route('/register')
class UserRegister(Resource):
    """User register resource"""

    @staticmethod
    @unauthorized_required
    @user_ns.expect(register_model)
    @user_ns.marshal_with(user_info_model, code=201)
    def post():
        """Provides creating new user"""
        try:
            new_user = register_schema.load(request.json, session=db.session)

            add_model_object(new_user)
            login_user(new_user)

            log_info()
        except ValidationError as error:
            log_error(error)
            return abort(422, error.messages)
        else:
            return new_user, 201


@current_app.before_request
def update_user_last_activity():
    """Updates user last_activity field before every request"""
    if current_user.is_authenticated:
        current_user.last_activity = datetime.now()
        db.session.commit()
