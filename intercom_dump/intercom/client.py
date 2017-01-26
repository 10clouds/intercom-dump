import itertools

import requests


class Client(object):
    base_url = 'https://api.intercom.io'
    base_args = dict(
        headers={'Accept': 'application/json'},
    )

    def __init__(self, app_id, api_key):
        self.app_id = app_id
        self.api_key = api_key

    @property
    def _requests_args(self):
        return dict(
            auth=(self.app_id, self.api_key),
            **self.base_args
        )

    def build_url(self, *path):
        return u'/'.join(itertools.chain((self.base_url,), path))

    def get(self, url, params=None):
        response = requests.get(url, params, **self._requests_args)
        response.raise_for_status()
        return response
