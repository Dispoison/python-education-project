"""User view module"""

from datetime import datetime

from flask import request, make_response, abort
from flask_login import login_user, current_user, logout_user
from flask_restx import Resource
from marshmallow.exceptions import ValidationError

from movie_library import app, api, db
from movie_library.models import login_model, register_model, user_info_model
from movie_library.schemes import LoginSchema, RegisterSchema
from movie_library.utils import AuthenticationError, \
    add_model_object, unauthorized_required, refresh_and_login_user

login_schema = LoginSchema()
register_schema = RegisterSchema()

user_ns = api.namespace(name='User', path='/user', description='user methods')


@user_ns.route('/login')
class UserLogin(Resource):
    """User login resource"""

    @unauthorized_required
    @user_ns.expect(login_model)
    def post(self):
        """Provides user authentication"""
        try:
            login = request.json.get('username_or_email')
            password = request.json.get('password')
            login_schema.validate_user_login(login, password)
            user = login_schema.authenticate_user(login, password)
        except ValidationError as error:
            return abort(400, error.messages)
        except AuthenticationError as error:
            return abort(401, str(error))
        else:
            refresh_and_login_user(user)
            return make_response({'message': 'Successfully authorized.'}, 200)


@user_ns.route('/logout')
class UserLogout(Resource):
    """User logout resource"""

    def post(self):
        """Provides user logout"""
        if current_user.is_authenticated:
            logout_user()
            return make_response({'message': 'Successfully logout.'}, 200)
        return make_response({'message': 'You cannot logout because you are not authorized.'}, 401)


@user_ns.route('/register')
class UserRegister(Resource):
    """User register resource"""

    @unauthorized_required
    @user_ns.expect(register_model)
    @user_ns.marshal_with(user_info_model, code=201)
    def post(self):
        """Provides creating new user"""
        try:
            new_user = register_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return abort(422, error.messages)
        else:
            add_model_object(new_user)
            login_user(new_user)
            return new_user, 201


@app.before_request
def update_user_last_activity():
    """Updates user last_activity field before every request"""
    if current_user.is_authenticated:
        current_user.last_activity = datetime.now()
        db.session.commit()
