from datetime import datetime
from flask import current_app, g

import requests

def get_strava():
    if 'strava' not in g:
        token = current_app.config['STRAVA']['ACCESS_TOKEN']
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

    ####
    # Returns the authenticated athlete profile from Strava
    ####
    def get_auth_athlete(self):
        url = f'{self.api_url}/athlete'
        r = requests.get(url, headers=self.headers)
        return r.json()

    ####
    # Returns athelete stats for run, ride, swim. All totals and ytd totals
    ####
    def get_athlete_stats(self, id):
        url = f'{self.api_url}/athletes/{id}/stats'
        r = request.get(url, headers=self.headers)
        return r.json()
    
    ####
    # return a range of activities between two timestampts.
    ####
    def get_activities(self, before=None, after=None, page=1, per_page=20):
        base_url = f'{self.api_url}athlete/activities'
        # end datetime of activity range
        if before is None:
            before = datetime.now().timestamp()
        # start datetime of activity range
        if after is None:
            after = datetime(2018, 7, 1, 0, 0).timestamp()
        params = f'?before={before}&after={after}&page={page}&per_page={per_page}'
        r = requests.get(f'{base_url}{params}', headers=self.headers)
        return r.json()
    
    ####
    # Returns the activities for the given year.
    ####
    def get_activities_by_year(self, year=datetime.now().year):
        # the start date of the year long range.
        after = datetime(year, 1, 1).timestamp()
        # the end date of the year long range
        before = datetime(year + 1, 1, 1).timestamp()
        return self.get_activities(before=before, after=after)
   
    ####
    # Returns the activities for the given month.
    ####
    def get_activities_by_month(self, year=datetime.now().year, month=datetime.now().month):
        # start date of month
        after = datetime(year, month, 1).timestamp()
        # end date of month
        if month == 13:
            month = 1
            year = year + 1
        before = datetime(year, month + 1, 1).timestamp()
        return self.get_activities(before=before, after=after)
