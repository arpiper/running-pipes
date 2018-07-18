import os
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the application
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance configuration, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # enable CORS
    CORS(app)

    # initialize the database
    from . import mdb
    mdb.init_app(app)

    # add the authorization blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # add the api blueprint
    from . import api
    app.register_blueprint(api.bp)

    return app
