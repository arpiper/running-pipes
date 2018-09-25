from datetime import datetime
from flask import current_app, g

import requests

def get_strava(token):
    if 'strava' not in g:
        #token = current_app.config['STRAVA']['ACCESS_TOKEN']
        g.strava = StravaAPI(token=token)
    return g.strava


class StravaAPI():
    api_url = 'https://www.strava.com/api/v3/'
    access_token = None
    headers = {
        'Content-type': 'application/json',
    }

    def __init__(self, token, **kwargs):
        self.access_token = token
        self.headers['Authorization'] = f'Bearer {token}'

    def get_auth_athlete(self):
        ''' 
        Retrieves authenticate athlete information from Strava
        
        :return: athlete dictionary 
        '''
        url = f'{self.api_url}/athlete'
        r = requests.get(url, headers=self.headers)
        return r.json(), r.status_code

    def get_athlete_stats(self, id):
        '''
        Retrieves ytd,mtd and other activity statistics of the current athlete

        :param int id: athlete id
        :return: athlete stats dictionary
        '''
        url = f'{self.api_url}/athletes/{id}/stats'
        r = requests.get(url, headers=self.headers)
        return r.json()
    
    def get_activities_all(self, before=None, after=None):
        '''
        Retrieve all strava activities between the given dates.

        :param int before: timestamp to end the range
        :param int after: timestamp to start the range
        :return: list of activities
        '''
        today = datetime.now()
        if before is None:
            before = today.timestamp()
        if after is None:
            day_index = today.isoweekday() if today.isoweekday() != 7 else 0 
            after = datetime(
                today.year, 
                today.month, 
                (today.day - day_index), 0, 0
            ).timestamp()
        pg = 1
        all_activities = []
        while 1:
            activities = self.get_activities(before=before, after=after, page=pg)
            # exit the infinite loop after all activities retreived
            if len(activities) == 0:
                break
            all_activities.extend(activities)
            pg += 1
        return all_activities

    def get_activities(self, before=None, after=None, page=1, per_page=30):
        '''
        Return the activities between after and before

        :param int before: timestamp to end the range
        :param int after: timestamp to start the range
        :param int page: page number of the activity list
        :param int per_page: number of activities per page
        :return: list of activities
        '''
        base_url = f'{self.api_url}athlete/activities'
        today = datetime.now()
        # end datetime of activity range
        if before is None:
            before = today.timestamp()
        # start datetime of activity range
        if after is None:
            after = datetime(
                today.year, 
                today.month, 
                (today.day - today.weekday()), 0, 0
            ).timestamp()
        params = f'?before={before}&after={after}&page={page}&per_page={per_page}'
        r = requests.get(f'{base_url}{params}', headers=self.headers)
        return r.json()
    
    def get_activities_by_year(self, year=datetime.now().year):
        '''
        get all activities by the given year.

        :param int year: the year to retrieve, defaults to this year
        :return: list of activities
        '''
        # the start date of the year long range.
        after = datetime(year, 1, 1).timestamp()
        # the end date of the year long range
        before = datetime(year + 1, 1, 1).timestamp()
        return self.get_activities(before=before, after=after)
   
    def get_activities_by_month(self, year=datetime.now().year, month=datetime.now().month):
        '''
        get all activities by given month and year

        :param int month: the month to retrieve, defaults to this month
        :param int year: the year to retrieve, defaults to this year
        :return: list of activities
        '''
        # start date of month
        after = datetime(year, month, 1).timestamp()
        # end date of month
        if month == 13:
            month = 1
            year = year + 1
        before = datetime(year, month + 1, 1).timestamp()
        return self.get_activities(before=before, after=after)


