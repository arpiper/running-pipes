from datetime import datetime as dt
from bson import ObjectId


class Goal():
    _id = None # ObjectId
    name = None # string
    userid = None # string/number strava athlete id
    type = 'distance' # string, [distance, time, pace]
    target = 0 # number in meters / seconds or meters per second
    target_m = 0 
    active = True # boolean, whether goal is complete or past end date
    start = None # string date 'yyyy-mm-dd'
    end = None # string date 'yyyy-mm-dd'
    activity = 'Run' # string [Run, Ride, Swim]
    # dictionary to track the goals progress
    progress = {
        'activity_cnt': 0,
        'activities': [],
        'current_duration': 0,
        'current_distance': 0,
        'percent_complete': 0,
        'most_recent': {
            'date': None,
            'id': 0, # strava activity id
        }
    }
    # Database connection to issue save/updates commands to 
    connection = None

    def __init__(self, goal, db):
        if db is None:
            raise ValueError('no db connection given to constructor')
        elif db.name == 'goals':
            self.connection = db
        else:
            self.connection = db.goals

        if '_id' in goal.keys():
            self._id = goal['_id']
        if 'start' not in goal.keys() or 'end' not in goal.keys():
            raise ValueError('goal must have valid start and end dats')
        #self.start = dt.fromisoformat(goal['start'])
        #self.end = dt.fromisoformat(goal['end'])
        self.start = dt.fromtimestamp(goal['start'])
        self.end = dt.fromtimestamp(goal['end'])
        if 'name' not in goal.keys():
            self.name = f'Goal ${goal["start"]} - ${goal["end"]}'
        self.name = goal['name']
        if 'userid' not in goal.keys():
            raise ValueError('no user associated with goal')
        self.userid = goal['userid']
        if 'type' in goal.keys():
            self.type = goal['type']
        if 'target' not in goal.keys():
            raise ValueError('goal must have a valid target')
        self.target = float(goal['target'])
        self.target_m = float(goal['target_m'])
        if 'active' in goal.keys():
            self.active = goal['active']
        if 'activity' in goal.keys():
            self.activity = goal['activity']
        if 'progress' in goal.keys():
            self.progress = goal['progress']

    def save(self):
        '''
        Save goal to the database
        '''
        if self._id is None:
            result = self.connection.insert_one(self.to_dict())
            self._id = result.inserted_id
        else:
            result = self.connection.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': self.to_dict()}
            )
        return self._id

    def to_dict(self):
        '''
        return a dictionary representation of the goal
        '''
        d = {
            'name': self.name,
            'userid': self.userid,
            'type': self.type,
            'target': self.target,
            'target_m': self.target_m,
            'active': self.active,
            'start': self.start.timestamp(),
            'end': self.end.timestamp(),
            'activity': self.activity,
            'progress': self.progress,
        }
        if self._id is not None:
            d['_id'] = self._id
        return d

    def check_end_date(self):
        '''
        Check whether the goal is past the end date 
        and update the active state

        :return: boolean
        '''
        today = dt.now().timestamp()
        end = dt.fromtimestamp(self.end)
        # today is greater than the end date, ie end date is in the past
        if today > end:
            self.active = False
            self.save()
        return self.active

    def update_progress(self, activities):
        '''
        Aggregate the activities for a total distance and time
        and other goal related statistics

        :param list activities: list of activities for the goal
        '''
        for act in activities:
            # guard against the wrong activities
            if act['type'] != self.activity:
                continue 

            # strip the Z. python datetime doesn't like it
            t = dt.fromisoformat(act['start_date_local'][:-1])
            # track the most recent activity for later updates
            if (not self.progress['most_recent']['date'] or 
                (self.progress['most_recent']['date'] < t.timestamp())):
                self.progress['most_recent']['date'] = t.timestamp()
                self.progress['most_recent']['id'] = act['id']

            # 1km = 0.621371 miles / 1 m = 0.000621371 miles
            # distance in meters
            self.progress['current_distance'] += act['distance'] 
            # time in seconds
            self.progress['current_duration'] += act['moving_time'] 
            # add the activity to array for tracking
            self.progress['activities'].append({
                'id': act['id'],
                'distance': act['distance'],
                'date': dt.fromisoformat(act['start_date_local'][:-1]),
                'moving_time': act['moving_time'],
            })
            self.progress['activity_cnt'] += 1

        # update the progress percentage
        if self.type == 'distance':
            self.progress['percent_complete'] = (100 
                * (self.progress['current_distance'] / self.target_m))
        elif self.type == 'time': 
            self.progress['percent_complete'] = (100 
                * (self.progress['current_duration'] / self.target_m))

        # cap the percent to 100%
        if self.progress['percent_complete'] > 100:
            self.progress['percent_complete'] = 100
            self.active = False

        self.save()
