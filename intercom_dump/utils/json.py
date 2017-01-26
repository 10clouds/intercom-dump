from __future__ import absolute_import

from contextlib import contextmanager
import json


@contextmanager
def write_array(stream):
    def write_item(obj):
        if write_item._index > 0:
            stream.write(', ')
        stream.write(json.dumps(obj))
        write_item._index += 1

    write_item._index = 0

    stream.write(u'[')
    try:
        yield write_item
    finally:
        stream.write(u']')
