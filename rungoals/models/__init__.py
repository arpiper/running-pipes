from .users import Users
from .goals import Goals
from flask import g
from ..services.mdb import get_db

def init_app(app):
    with app.app_context():
        db = get_db().db
        Users.init_app(Users, db)
        Goals.init_app(Goals, db)
