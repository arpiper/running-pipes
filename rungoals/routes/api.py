import calendar
from flask import Blueprint, flash, g, redirect, request, url_for, jsonify, current_app, abort
from werkzeug.exceptions import abort
from bson import ObjectId
from datetime import datetime as dt
import functools
import requests

from .auth import login_required
from ..services.mdb import get_db
from ..services.stravaAPI import get_strava
from ..models.goals import Goals
from ..models.goal import Goal

api_bp = Blueprint('api', __name__, url_prefix='/api')
goals = Goals()
test = 'before'

# decorator
def validate_auth(func):
    @functools.wraps(func)
    def wrapper_validate_auth(*args, **kwargs):
        if 'Authorization' not in request.headers.keys():
            abort(401)
        kwargs['auth'] = request.headers.get('Authorization').split(' ')[1]
        return func(*args, **kwargs)
    return wrapper_validate_auth


@api_bp.route('/auth', methods=['POST'])
def get_token():
    cs = current_app.config['STRAVA']['CLIENT_SECRET']
    cid = current_app.config['STRAVA']['CLIENT_ID']
    body = request.get_json()
    if 'code' not in body.keys():
        return jsonify({
            'message': 'invalid code'
        }), 401
    r = requests.post(
        'https://www.strava.com/oauth/token',
        data = {
            'client_id': cid,
            'client_secret': cs,
            'code': body['code']
        }
    )
    return jsonify(r.json()), r.status_code

@api_bp.route('/athlete', methods=['GET'])
@validate_auth
def get_athlete(**kwargs):
    auth = request.headers['authorization'].split(' ')[1]
    st = get_strava(auth)
    athlete, status = st.get_auth_athlete()
    r = {}
    # Strava api returned 401
    if status == 401:
        r['message'] = athlete['message']
        r['data'] = {
            'errors': athlete['errors']
        }
    else: 
        r['message'] = f'Athlete information retrieved'
        r['data'] = {
            'athlete': athlete
        }
    return jsonify(r), status

@api_bp.route('/data/<id>', methods=['GET'])
@validate_auth
def get_data(id, **kwargs):
    g = goals.get_one(id)
    return jsonify({
        'message': 'api get datae',
        'data': {
            'sti': 'THE DATA',
            'goal': g
        }
    })

@api_bp.route('/activities', methods=['GET'])
@validate_auth
def get_activities(**kwargs):
    auth = request.headers['authorization'].split(' ')[1]
    st = get_strava(auth)
    data = st.get_activities()
    return jsonify({
        'message': 'this weeks activites',
        'data': {
            'activities': data,
        }
    })

@api_bp.route('/goals', methods=['GET', 'POST'])
@validate_auth
def get_goals(**kwargs):
    auth = request.headers.get('authorization').split(' ')[1]
    if request.method == 'GET':
        if 'userid' not in request.args.keys():
            return jsonify({
                'message': 'error retrieving goals',
                'data': {
                    'error': 'no user id given',
                }
            })
        st = get_strava(auth)
        goals = Goals()
        goal_list, oldest = goals.get_many(request.args['userid'])

        activities = st.get_activities_all(after=oldest, before=dt.now().timestamp())
        updated = []
        for goal in goal_list:
            if goal.check_end_date():
                goal.update_progress(activities)
            updated.append(goal.to_dict())

        return jsonify({
            'message': 'get all the running goals',
            'data': {
                'goals': updated,
            },
        })
    elif request.method == 'POST':
        data = request.get_json()
        if not data: 
            return jsonify({
                'message': 'invalid data given',
            })
        db = get_db()
        st = get_strava(auth)
        goal = Goal(data, db.db)
        activities = st.get_activities_all(
            after=goal.start.timestamp(), 
            before=goal.end.timestamp()
        )
        goal.update_progress(activities)
        return jsonify({
            'message': 'new goal added',
            'data': {
                'id': goal._id,
                'goal': goal.to_dict()
            },
        })

@api_bp.route('/goals/<id>', methods=['GET'])
@validate_auth
def get_goal(id, **kwargs):
    goal = goals.get_one(id)
    today = dt.now()
    auth = request.headers.get('authorization').split(' ')[1]
    st = get_strava(auth)
    if goal.progress['most_recent']['date'] is None:
        activities = st.get_activities_all(
            before=today.timestamp(),
            after=goal.start.timestamp()
        )
        goal.update_progress(activities)
    elif (goal.active 
        and goal.progress['most_recent']['date'] < today.timestamp()):
        activities = st.get_activities_all(
            before=today.timestamp(),
            after=goal.progress['most_recent']['date']
        )
        goal.update_progress(activities)
    return jsonify({
        'message': 'get a single running goal with the id',
        'data': {
            'goal': goal.to_dict(),
        },
    })

@api_bp.route('/goals/<int:year>', methods=['GET'])
@validate_auth
def get_goals_year(year, **kwargs):
    auth = request.headers.get('authorization').split(' ')[1]
    st = get_strava(auth)
    data = st.get_activities_by_year(year)
    return jsonify({
        'message': f'get all running activities for {year}',
        'data': {
            'year': year,
            'activities': data,
        },
    })

@api_bp.route('/goals/<int:year>/<int:month>', methods=['GET'])
@validate_auth
def get_goals_month(year, month, **kwargs):
    auth = request.headers.get('authorization').split(' ')[1]
    st = get_strava(auth)
    data = st.get_activities_by_month(year, month)
    return jsonify({
        'message': f'get all running activities for {calendar.month_name[month]} {year}',
        'data': {
            'year': year,
            'month': {
                'name': calendar.month_name[month],
                'idx': month,
            },
            'activities': data,
        },
    })

@api_bp.route('/goals/refresh', methods=['POST'])
@validate_auth
def update_goals_progress(**kwargs):
    data = request.get_json()
    if 'userId' not in data:
        return jsonify({
            'message': 'error updated goals, no userid'
        })
    goal_list, oldest = goals.get_many(data['userId'])
    auth = request.headers.get('authorization').split(' ')[1]
    return jsonify({
        'message': 'goals refreshed',
        'data': {
            'goals': updated,
        },
    })

@api_bp.route('/stats/<int:athleteid>', methods=['GET'])
@validate_auth
def get_stats(athleteid, **kwargs):
    auth = request.headers.get('authorization').split(' ')[1]
    st = get_strava(auth)
    data = st.get_athlete_stats(athleteid)
    return jsonify({
        'message': f'retrieving athlete {athleteid} statistics',
        'data': {
            'stats': data,
        }
    })


