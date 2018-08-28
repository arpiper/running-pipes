from pymongo import MongoClient
from flask_pymongo import PyMongo
from ..models.users import Users

from flask import current_app, g


def get_db():
    if 'mongo' not in g:
        # requires MONGO_URI exists in the app config
        g.mongo = PyMongo(current_app)

    # return the reference to the database
    return g.mongo


def init_app(app):
    # cleanup called after response is returned
    #app.teardown_appcontext()
    pass
