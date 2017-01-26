from datetime import datetime
import itertools
import logging

import gevent
import requests


log = logging.getLogger(__name__)


class Client(object):
    base_url = 'https://api.intercom.io'
    base_args = dict(
        headers={'Accept': 'application/json'},
    )
    base_rate_limit = 500

    def __init__(self, app_id, api_key):
        self.app_id = app_id
        self.api_key = api_key

        self.rate_limit = self.base_rate_limit
        self.rate_remaining = self.rate_limit
        self.rate_limited_until = datetime(2000, 1, 1)

    @property
    def _requests_args(self):
        return dict(
            auth=(self.app_id, self.api_key),
            **self.base_args
        )

    def build_url(self, *path):
        return u'/'.join(itertools.chain((self.base_url,), path))

    @property
    def is_rate_limited(self):
        return self.rate_remaining == 0

    def _ready_in(self):
        if self.is_rate_limited:
            delta = self.rate_limited_until - datetime.utcnow()
            return max(delta.total_seconds(), 30)
        else:
            return 0

    def _wait_until_ready(self):
        while self.is_rate_limited:
            limited_until = self.rate_limited_until

            gevent.sleep(self._ready_in())

            reset_limit = (
                self.rate_limited_until == limited_until and
                self.rate_remaining == 0
            )

            if reset_limit:
                log.info('Resuming...')
                self.rate_remaining = self.rate_limit

        self.rate_remaining = max(self.rate_remaining - 1, 0)

    def _was_rate_limited(self, response):
        if response.status_code != 429:
            return False

        until_timestamp = int(response.headers['X-RateLimit-Reset'])
        until = datetime.utcfromtimestamp(until_timestamp)

        if until > self.rate_limited_until:
            log.info(u'Rate limited until %s', until)

        self.rate_limited_until = until
        self.rate_limit = int(response.headers['X-RateLimit-Limit'])
        self.rate_remaining = 0
        return True

    def get(self, url, params=None):
        retry = True

        while retry:
            self._wait_until_ready()
            response = requests.get(url, params, **self._requests_args)
            retry = self._was_rate_limited(response)

        response.raise_for_status()
        return response
