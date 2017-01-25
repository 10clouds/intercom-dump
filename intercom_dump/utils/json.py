from __future__ import absolute_import

import json


def dumps_iterable(iterable):
    yield u'['

    try:
        for index, item in enumerate(iterable):
            if index > 0:
                yield ', '

            yield json.dumps(item)
    finally:
        yield u']'
