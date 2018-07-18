from flask import Blueprint, flash, g, redirect, request, url_for, jsonify, current_app
from werkzeug.exceptions import abort

from .auth import login_required
from .mdb import get_db
from .stravaAPI import StravaAPI

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/data', methods=['GET'])
def get_data():
    db = get_db()
    return jsonify({
        'message': 'api get datae',
        'data': 'THE DATA',
        'db': db.collection_names(),
    })

@bp.route('/goals', methods=['GET'])
def get_goals():
    strava = StravaAPI(token=current_app.config['STRAVA']['ACCESS_TOKEN'])
    #data = get_activities(token=current_app.config['STRAVA']['ACCESS_TOKEN'])
    data = strava.get_activities()
    return jsonify({
        'message': 'get all the running goals',
        'data': data,
    })


@bp.route('/goals/<int:id>', methods=['GET'])
def get_goal(id):
    return jsonify({
        'message': 'get a single running goal with the id',
        'data': {
            'goalid': id,
            'goal': 'GOOAAAAAL!',
        },
    })
