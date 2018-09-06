from bson import ObjectId
from datetime import datetime as dt

from ..services.stravaAPI import get_strava

class Goals(dict):
    connnection = None
    strava = None

    def init_app(self, connection):
        '''
        Initialize the Goal class

        :param Mongo.DB connection: Mongo Database connection
        '''
        self.connection = connection.goals
        self.strava = get_strava()

    def save(self, goal):
        '''
        Save goal to the database

        :param dict goal: a goal
        '''
        if '_id' not in goal.keys():
            resultid = self.connection.insert_one(goal).inserted_id
        else:
            resultid = self.connection.update_one(
                {'_id': ObjectId(goal['_id'])}, 
                goal
            ).upserted_id
        return resultid

    def get_one(self, goalid):
        '''
        Retrieve a goal from the database

        :param str goalid: MongoDB goal id string
        :return: goal dict
        '''
        return self.connection.find_one({
            '_id': ObjectId(goalid)
        })

    def get_many(self, userid):
        '''
        Retrieve all goals related to a user

        :param int userid: Strava user id
        :return: list of goals
        '''
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
        '''
        Create a new goal object

        :param dict goal: Initial goal data
        :return: the new goal
        '''
        goal['target'] = float(goal['target'])
        goal['progress'] = self.update_goal_progress(goal)

        return self.save(goal)


    def update_goal_progress(self, goal):
        '''
        Grab the activities within the goal dates and update the progress.

        :param dict goal: goal dictionary
        :return: goal
        '''
        start = dt.fromisoformat(goal['start'])
        if 'progress' in goal.keys():
            start = dt.fromisoformat(goal['progress']['most_recent']['date'])
        end = dt.fromisoformat(goal['end'])
        page = 1
        all_activities = []
        while 1:
            # fetch the activities from the Strava API
            activities = self.strava.get_activities(
                before=end.timestamp(),
                after=start.timestamp(),
                page=page,
                per_page=50
            )
            # check if the result is empty
            if len(activities) == 0:
                break
            all_activities.extend(activities)
            # increment the page for the next call to Strava API
            page += 1
        if 'progress' in goal.keys():
            return self.aggregate_activities(all_activities, 
                goal['target'], 'Run', goal['type'], goal['progress'])
        return self.aggregate_activities(all_activities, goal['target'], 'Run', goal['type'])
        

    def aggregate_activities(self, activities, target, act_type, goal_type, p=None):
        '''
        Aggregate the activities for a total distance and time
        and other goal related statistics

        :param list activities: list of activities for the goal
        :param int target: goal target
        :param str act_type: activity type
        :param str goal_type: goal type
        :param dict p: (optional) goal progress 
        :return: dict progress
        '''
        # initialize the empty p dict if no goal['progress'] dict passed
        if not p:
            p = {
                'activity_cnt': 0,
                'activities': [],
                'current_duration': 0,
                'current_distance': 0,
                'percent_complete': 0,
                'most_recent': {
                    'date': None,
                    'id': 0,
                }
            }
        for act in activities:
            # guard against the wrong activities
            if act['type'] != activity_type:
                continue 

            # strip the Z. python datetime doesn't like it
            t = act['start_date_local'][:-1] 
            # track the most recent activity for later updates
            if (not p['most_recent']['date'] or 
                (p['most_recent']['date'].timestamp() 
                < dt.fromisoformat(t).timestamp())):
                p['most_recent']['date'] = dt.fromisoformat(t)
                p['most_recent']['id'] = act['id']

            # 1km = 0.621371 miles / 1 m = 0.000621371 miles
            # convert the distance from meters to miles
            p['current_distance'] += (act['distance'] * 0.000621371)
            p['current_duration'] += act['moving_time'] # time in seconds
            p['activities'].append({
                'id': act['id'],
                'distance': act['distance'] * 0.000621371,
                'date': act['start_date_local'],
                'moving_time': act['moving_time'],
            })
            p['activity_cnt'] += 1
        if goal_type == 'distance':
            p['percent_complete'] = 100 * (p['current_distance'] / target)
        elif goal_type == 'time': 
            p['percent_complete'] = 100 * (p['current_duration'] / target)
        return p
