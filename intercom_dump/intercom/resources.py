from .resource import (
    PaginatedMixin,
    Resource,
    WithNestedMixin,
)


class Users(WithNestedMixin, PaginatedMixin, Resource):
    name = 'users'


class PerUserMixin(object):
    def __init__(self, client, user, params=None):
        super(PerUserMixin, self).__init__(client, params=params)

        user_id = user['user_id'] if isinstance(user, dict) else user

        self.params.update(
            type='user',
            user_id=user_id,
        )


class UserNotes(PerUserMixin, PaginatedMixin, Resource):
    name = 'notes'


class UserEvents(PerUserMixin, PaginatedMixin, Resource):
    name = 'events'
    pages_next_key = 'since'


class Contacts(PaginatedMixin, Resource):
    name = 'contacts'


Leads = Contacts


class Companies(PaginatedMixin, Resource):
    name = 'companies'


class Tags(PaginatedMixin, Resource):
    name = 'tags'


class Segments(PaginatedMixin, Resource):
    name = 'segments'


class Conversations(PaginatedMixin, Resource):
    name = 'conversations'


class ConversationsWithParts(Conversations):
    def __iter__(self):
        for conversation in super(Conversations, self).__iter__():
            conversation_url = self.retrieve_url(conversation['id'])
            yield self.client.get(conversation_url).json()
