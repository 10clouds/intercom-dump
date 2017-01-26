from .resource import (
    build_resource,
    iter_paginated_resource,
    register,
)


users = build_resource('users')


def user_filter(user):
    user_id = user['user_id'] if isinstance(user, dict) else user
    return dict(type='user', user_id=user_id)


@register('users.notes')
def user_notes(client, user):
    return iter_paginated_resource(client, 'notes', user_filter(user))


@register('users.events')
def user_events(client, user):
    return iter_paginated_resource(
        client,
        'events',
        user_filter(user),
        next_key='since',
    )


admins = build_resource('admins')
contacts = build_resource('contacts', register='leads')
companies = build_resource('companies')
tags = build_resource('tags')
segments = build_resource('segments')
conversations = build_resource('conversations')


@register('conversations.conversation_parts')
def conversation_parts(client, conversation):
    url = client.build_url('conversations', conversation['id'])
    conversation = client.get(url).json()
    return conversation['conversation_parts']['conversation_parts']
