import functools
from flask import Blueprint, g, flash, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from rungoals.mdb import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        return {
            'message': 'new user registered', 
            'data': 'None'
        }

    return jsonify({
        'message': 'Register a new user here',
        'data': None
    })


@bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        return jsonify({
            'message': 'user logged id',
            'data': 'post'
        })
    return jsonify({
        'message': 'log in a user',
        'data': 'get'
    })


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
