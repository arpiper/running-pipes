import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

class JSONEncoder(json.JSONEncoder):
    '''extend the json-encoder class'''
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


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

    # use the modified json encoder
    app.json_encoder = JSONEncoder

    # enable CORS
    CORS(app)

    # initialize the database
    from . import services
    services.init_app(app)

    # import and initialize the routes with the app
    from . import routes 
    routes.init_app(app)

    from . import models 
    models.init_app(app)

    return app
