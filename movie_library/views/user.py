"""User view module"""

from datetime import datetime

from flask import request, make_response, abort
from flask_login import login_user, current_user, logout_user
from flask_restx import Resource
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from movie_library import app, api, db
from movie_library.models import User, login_model, register_model, user_info_model
from movie_library.schemes import UserSchema
from movie_library.utils import add_model_object


user_schema = UserSchema()

user_ns = api.namespace(name='User', path='/user', description='user methods')


@user_ns.route('/login')
class UserLogin(Resource):
    """User login resource"""
    @user_ns.expect(login_model)
    def post(self):
        """Provides user authentication"""
        if current_user.is_authenticated:
            return make_response({'message': f'You are already logged in '
                                             f'as {current_user.username}.'}, 400)
        username_or_email = request.json['username_or_email']
        password = request.json['password']

        if username_or_email and password:
            user = User.query.filter(or_(User.username == username_or_email,
                                         User.email == username_or_email)).first()

            if user and check_password_hash(user.password, password):
                user.last_activity = datetime.now()
                db.session.commit()
                login_user(user)
                return make_response({'message': 'Successfully authorized.'}, 200)

            return make_response({'message': 'Username or password are incorrect.'}, 401)

        return make_response({'message': 'Fill in the username and password fields.'}, 401)


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
    @user_ns.expect(register_model)
    @user_ns.marshal_with(user_info_model, code=201)
    def post(self):
        """Provides creating new user"""
        if current_user.is_authenticated:
            return abort(400, f'You are already logged in as {current_user.username}.')

        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        password2 = request.json.get('password2')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')

        if all([username, email, password, password2, first_name, last_name]):
            user_by_username = User.query.filter_by(username=username).first()
            if user_by_username:
                return abort(409, 'Username already exists.')

            user_by_email = User.query.filter_by(email=email).first()
            if user_by_email:
                return abort(409, 'Email already exists.')

            if password != password2:
                return abort(400, 'Passwords are not equal.')

            hash_pwd = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hash_pwd,
                            first_name=first_name, last_name=last_name)
            login_user(new_user)
            return add_model_object(new_user)

        return abort(400, 'Fill in the username, email, password, password2, '
                          'first_name and last_name fields.')


@app.before_request
def update_user_last_activity():
    """Updates user last_activity field before every request"""
    if current_user.is_authenticated:
        current_user.last_activity = datetime.now()
        db.session.commit()
