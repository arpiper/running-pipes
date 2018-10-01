from bson import ObjectId
from datetime import datetime as dt

from ..services.stravaAPI import get_strava
from .goal import Goal

class Goals(dict):
    connnection = None
    strava = None

    def __init__(self):
        #self.strava = get_strava()
        super()

    def init_app(self, connection):
        '''
        Initialize the Goal class

        :param Mongo.DB connection: Mongo Database connection
        '''
        self.connection = connection.goals
        #self.strava = get_strava(token)

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
        g = self.connection.find_one({
            '_id': ObjectId(goalid)
        })
        goal = Goal(g, self.connection)
        return goal

    def get_many(self, userid):
        '''
        Retrieve all goals related to a user

        :param int userid: Strava user id
        :return: list of goals, and date of oldest most recent activity
        '''
        if type(userid) == str: 
            userid = int(userid)
        cursor = self.connection.find({
            'userid': userid,
        })
        goals = []
        oldest = dt.now().timestamp()
        for goal in cursor:
            if (goal['progress']['most_recent']['date'] is not None
                and goal['progress']['most_recent']['date'] < oldest):
                oldest = goal['progress']['most_recent']['date']
            goals.append(Goal(goal, self.connection))
        return goals, oldest

    def create_goal(self, goal):
        '''
        Create a new goal object

        :param dict goal: Initial goal data
        :return: the new goal
        '''
        goal['target'] = float(goal['target'])
        goal['progress'] = self.update_goal_progress(goal)

        return self.save(goal)

    def update_goal(self, goal):
        '''
        Update the goal with the current progress.

        :param dict goal: the goal to update.
        :return: str goal id
        '''
        progress = self.update_goal_progress(goal)
        goal['progress'] = progress
        if goal['progress']['percent_complete'] == 100:
            goal['active'] = False
        return self.save(goal)

    def get_goals_by_month(self, year=None, month=None):
        '''
        Retrieve goals that occur in the given month

        :param int year: the year to search
        :param int month: the month to search
        :return: list of the goals
        '''
        today = dt.now()
        if year is None:
            year = today.year
        if month is None:
            month = today.month
        start = dt(year, month, 1, 0, 0)
        end = dt(year, month + 1, 1, 0, 0)
        cursor = self.connection.find(
            {'start': { '$gt': start.timestamp() }},
            {'end': { '$lt': end.timestamp() }}
        )
        goals = []
        for goal in cursor:
            goals.append(goal)
        return goals

    def get_goals_by_year(self, year=None):
        '''
        Retrieve the goals that occur in the given year

        :param int year: the year to search 
        :return: list of the goals
        '''
        today = dt.now()
        if year is None:
            year = today.year
        start = dt(year, 1, 1, 0, 0)
        end = dt(year + 1, 1, 1, 0, 0)
        cursor = self.connection.find(
            {'start': { '$gt': start.timestamp() }},
            {'end': { '$lt': end.timestamp() }}
        )
        goals = []
        for goal in cursor:
            goals.append(goal)
        return goals
