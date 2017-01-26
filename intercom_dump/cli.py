# -*- coding: utf-8 -*-

import click

from .intercom import resources as _  # noqa
from .intercom.client import Client
from .intercom.resource import (
    iter_objects,
    registry,
)
from .utils.json import dumps_iterable


@click.command()
@click.argument(
    'resources',
    nargs=-1,
    type=click.Choice(registry.keys()),
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
def main(resources, app_id, api_key, format):
    """
    Dumps intercom objects
    """

    if app_id and api_key:
        client = Client(app_id, api_key)
    else:
        raise click.UsageError(u'You must either specify app id and api key')

    stdout = click.get_text_stream('stdout')
    for data in dumps_iterable(iter_objects(client, resources)):
        stdout.write(data)


if __name__ == "__main__":
    main()
