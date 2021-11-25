"""Movie library application"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

from movie_library.log import Log
from config import env

db = SQLAlchemy()
migrate = Migrate()
api = Api()
ma = Marshmallow()
login_manager = LoginManager()
log = Log()


def create_app(config: str):
    app = Flask(__name__)
    app.config.from_object(env.get(config, env['default']))
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    api.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    log.init_app(app)

    with app.app_context():
        from movie_library import models
        from movie_library import views

        from commands import add_commands
        add_commands(app)

        login_manager.anonymous_user = models.AnonymousUser
    return app
