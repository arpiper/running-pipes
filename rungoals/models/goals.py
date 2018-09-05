from bson import ObjectId
from datetime import datetime as dt

from ..services.stravaAPI import get_strava

class Goals(dict):
    connnection = None
    strava = None

    def init_app(self, connection):
        self.connection = connection.goals
        self.strava = get_strava()

    def save(self, goal):
        if '_id' not in goal.keys():
            resultid = self.connection.insert_one(goal).inserted_id
        else:
            resultid = self.connection.update_one(
                {'_id': ObjectId(goal['_id'])}, 
                goal
            ).upserted_id
        return resultid

    def get_one(self, goalid):
        return self.connection.find_one({
            '_id': ObjectId(goalid)
        })

    def get_many(self, userid):
        if type(userid) == str: 
            userid = int(userid)
        cursor = self.connection.find({
            'userid': userid,
        })
        goals = []
        for goal in cursor:
            goals.append(goal)
        return goals

    def create_goal(self, goal):
        goal['target'] = float(goal['target'])
        if goal['type'] == 'distance':
            goal['progress'] = self.update_goal_progress(goal)

        return self.save(goal)

    ##
    # grab all the relavent activities and update the progress towards it.
    ##
    def update_goal_progress(self, goal):
        start = dt.fromisoformat(goal['start'])
        if 'progress' in goal.keys():
            start = dt.fromisoformat(goal['progress']['most_recent']['date'])
        end = dt.fromisoformat(goal['end'])
        page = 1
        all_activities = []
        while 1:
            activities = self.strava.get_activities(
                before=end.timestamp(),
                after=start.timestamp(),
                page=page,
                per_page=50
            )
            if len(activities) == 0:
                break
            all_activities.extend(activities)
        if 'progress' in goals.keys():
            return self.aggregate_activities(all_activities, 
                goal['target'], 'Run', goal['progress'])
        return self.aggregate_activities(all_activities, goal['target'], 'Run')
        
    ##
    # aggregate the activities for a total distance 
    # and other goal related stats
    ##
    def aggregate_activities(self, activities, target, goal_type, p=None):
        # initialize the empty p dict if no goal['progress'] dict passed
        if not p:
            p = {
                'activity_cnt': 0,
                'activities': [],
                'current_distance': 0,
                'percent_complete': 0,
                'most_recent': {
                    'date': None,
                    'id': 0,
                }
            }
        for act in activities:
            if act['type'] == goal_type:
                # strip the Z. python datetime doesn't like it
                t = act['start_date_local'][:-1] 
                # track the most recent activity for later updates
                if (not p['most_recent']['date'] or 
                    (p['most_recent']['date'].timestamp() 
                    < dt.fromisoformat(t).timestamp())):
                    p['most_recent']['date'] = dt.fromisoformat(t)
                    p['most_recent']['id'] = act['id']

                # 1km = 0.621371 miles / 1 m = 0.000621371 miles
                p['current_distance'] += (act['distance'] * 0.000621371)
                p['activities'].append({
                    'id': act['id'],
                    'distance': act['distance'] * 0.000621371,
                    'date': act['start_date_local'],
                    'moving_time': act['moving_time'],
                })
                p['activity_cnt'] += 1
        p['percent_complete'] = 100 * (p['current_distance'] / target)
        return p
