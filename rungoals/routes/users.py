import os
from flask import Blueprint, request, jsonify, current_app
from ..services.mdb import get_db
from ..models.users import Users
#import logger

''' controller and routes for users '''

user_bp = Blueprint('users', __name__, url_prefix='/api')

@user_bp.route('/users', methods=['GET'])
def user():
    query = request.args
    mongo = get_db()
    #data = mongo.db.name
    data = Users.get_one(Users, 1)
    return jsonify(data), 200
