import os
from os.path import join, dirname, realpath
import uuid

from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/images/recipes/')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI='sqlite:///' +
        os.path.join(app.instance_path, 'yummyshare.sqlite'),
        UPLOAD_FOLDER=UPLOADS_PATH,
        MAX_CONTENT_LENGTH=16 * 1024 * 1024
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from yummyshare.auth.views import bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from yummyshare.recipe.views import bp as recipe_blueprint
    app.register_blueprint(recipe_blueprint)

    login_manager.init_app(app)
    login_manager.login_message = 'You must be logged in to access.'
    login_manager.login_view = 'auth.login'

    return app
