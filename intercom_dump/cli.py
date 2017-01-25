# -*- coding: utf-8 -*-

import click

from .intercom.client import Client
from .intercom.resources import (
    Companies,
    Contacts,
    PerUserMixin,
    Segments,
    Tags,
    UserEvents,
    UserNotes,
    Users,
)
from .intercom.resources import ConversationsWithParts as Conversations
from .utils.json import dumps_iterable


RESOURCES_BY_NAME = {
    resource.name: resource
    for resource in (
        Companies,
        Contacts,
        Conversations,
        Segments,
        Tags,
        UserEvents,
        UserNotes,
        Users,
    )
}


@click.command()
@click.argument(
    'resources',
    nargs=-1,
    type=click.Choice(RESOURCES_BY_NAME.keys()),
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
    type=click.Choice(('json', 'csv')),
)
def main(resources, app_id, api_key, format):
    """
    Dumps intercom objects
    """

    if app_id and api_key:
        client = Client(app_id, api_key)
    else:
        raise click.UsageError(u'You must either specify app id and api key')

    global_resource_classes = []
    per_user_resource_classes = []

    for resource_name in resources:
        resource_class = RESOURCES_BY_NAME[resource_name]

        if issubclass(resource_class, PerUserMixin):
            per_user_resource_classes.append(resource_class)
        else:
            global_resource_classes.append(resource_class)

    for resource_class in global_resource_classes:
        if resource_class is Users:
            resource = resource_class(
                client,
                nested_classes=set(per_user_resource_classes),
            )
        else:
            resource = resource_class(client)

        for data in dumps_iterable(resource):
            click.echo(data)


if __name__ == "__main__":
    main()
