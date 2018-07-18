from datetime import datetime

import requests

class StravaAPI():
    api_url = 'https://www.strava.com/api/v3/'
    access_token = None
    headers = {
        'Content-type': 'application/json',
    }

    def __init__(self, token, **kwargs):
        self.access_token = token
        self.headers['Authorization'] = f'Bearer {token}'

    def get_activities(self, before=None, after=None, page=1, per_page=20):
        base = f'{self.api_url}athlete/activities'
        if before is None:
            before = datetime.now().timestamp()
        if after is None:
            after = datetime(2018, 7, 1, 0, 0).timestamp()
        params = f'?before={before}&after={after}&page={page}&per_page={per_page}'
        r = requests.get(f'{base}{params}', headers=self.headers)
        return r.json()
