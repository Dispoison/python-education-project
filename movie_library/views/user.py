from datetime import datetime

from flask import request, make_response
from flask_login import login_user, current_user, logout_user, login_required
from flask_restx import Resource
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from movie_library import app, api, db
from movie_library.models import User
from movie_library.schema import UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@api.route('/login')
class UserLogin(Resource):
    def post(self):
        if current_user.is_authenticated:
            return make_response({'message': f'You are already logged in as {current_user.username}.'}, 400)
        username_or_email = request.json['username_or_email']
        password = request.json['password']

        if username_or_email and password:
            user = User.query.filter(or_(User.username == username_or_email, User.email == username_or_email)).first()

            if user and check_password_hash(user.password, password):
                user.last_activity = datetime.now()
                db.session.commit()
                login_user(user)
                return make_response({'message': 'Successfully authorized.'}, 200)
            else:
                return make_response({'message': 'Username or password are incorrect.'}, 401)
        return make_response({'message': 'Fill in the username and password fields.'}, 401)


@api.route('/logout')
class UserLogout(Resource):
    @login_required
    def post(self):
        logout_user()
        return make_response({'message': 'Successfully logout.'}, 200)


@api.route('/register')
class UserRegister(Resource):
    def post(self):
        if current_user.is_authenticated:
            return make_response({'message': f'You are already logged in as {current_user.username}.'}, 400)

        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        password2 = request.json['password2']
        first_name = request.json['first_name']
        last_name = request.json['last_name']

        if username and email and password and password2 and first_name and last_name:
            user_by_username = User.query.filter_by(username=username).first()
            if user_by_username:
                return make_response({'message': 'Username already exists.'}, 409)

            user_by_email = User.query.filter_by(email=email).first()
            if user_by_email:
                return make_response({'message': 'Email already exists.'}, 409)

            if password != password2:
                return make_response({'message': 'Passwords are not equal.'}, 400)

            hash_pwd = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hash_pwd,
                            first_name=first_name, last_name=last_name)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return make_response({'message': 'Successfully registered.'}, 200)
        else:
            return make_response({'message': 'Fill in the username, email, password, first and last name fields.'}, 401)


@app.before_request
def update_user_last_activity():
    if current_user.is_authenticated:
        current_user.last_activity = datetime.now()
        db.session.commit()
