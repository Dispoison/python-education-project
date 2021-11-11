from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
ma = Marshmallow(app)

from movie_library import views
from movie_library import models
