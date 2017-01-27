# -*- coding: utf-8 -*-

from gevent import monkey  # noqa
monkey.patch_all()         # noqa

import logging

import click
import gevent
import six

from .intercom import resources as _  # noqa
from .intercom.client import Client
from .intercom.resource import (
    prepare_resources,
    registry,
)
from .utils.json import write_array


@click.command()
@click.argument(
    'resources',
    nargs=-1,
    type=click.Choice(list(six.iterkeys(registry)) + ['all']),
)
@click.option(
    '--app-id',
    envvar='INTERCOM_APP_ID',
    help='App id',
)
@click.option(
    '--api-key',
    envvar='INTERCOM_API_KEY',
    help='Api key',
)
@click.option(
    '--format',
    default='json',
    type=click.Choice(('json',)),
)
@click.option(
    '-v',
    '--verbose',
    count=True,
)
def main(resources, app_id, api_key, format, verbose):
    """
    Dumps intercom objects
    """

    if verbose == 0:
        log_level = logging.WARN
    elif verbose == 1:
        log_level = logging.INFO
    elif verbose >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)

    if app_id and api_key:
        client = Client(app_id, api_key)
    else:
        raise click.UsageError(u'You must either specify app id and api key')

    if 'all' in resources:
        resources = list(six.iterkeys(registry))

    stdout = click.get_text_stream('stdout')
    resources = prepare_resources(client, resources)

    with write_array(stdout) as write_item:
        def write_resource(resource):
            for obj in resource(client):
                write_item(obj)

        gevent.joinall([
            gevent.spawn(write_resource, resource)
            for resource in resources
        ])


if __name__ == "__main__":
    main()
