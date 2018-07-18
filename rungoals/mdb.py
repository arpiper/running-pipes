from pymongo import MongoClient

from flask import current_app, g


def get_db():
    if 'db' not in g:
        if 'DATABASE' in current_app.config.keys():
            auth = current_app.config['DATABASE']
            cs = f"mongodb://{auth['user']}:{auth['pass']}@{auth['host']}:{auth['port']}/{auth['auth']}"
            g.db = MongoClient(cs)
        else:
            g.db = MongoClient()

    return g.db.runningGoals


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
