"""Movie library application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

from movie_library.log import Log

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
api = Api(app)
ma = Marshmallow(app)
login_manager = LoginManager(app)
log = Log(app)

from movie_library import models
from movie_library import views

from commands import add_commands
add_commands(app)

login_manager.anonymous_user = models.AnonymousUser
