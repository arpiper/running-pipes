from pymongo import MongoClient

from flask import current_app, g


def get_db():
    if 'db' not in g:
        auth = current_app['DATABASE']
        g.db = MongoClient(
            f"mongodb://{auth['user']}:{auth['pass']}@{auth['host']}:{auth['port']}/{auth['auth']}"
        )

    return g.db.runningGoals


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
