BASE_URL = 'https://api.intercom.io'

LIST_URL_TEMPLATE = u'/'.join((BASE_URL, '{name}'))
RETRIEVE_URL_TEMPLATE = u'/'.join((BASE_URL, '{name}', '{id}'))


class Resource(object):
    name = None

    def __init__(self, client, params=None):
        self.client = client
        self.params = params.copy() if params else {}

    def list_url(self):
        return LIST_URL_TEMPLATE.format(name=self.name)

    def retrieve_url(self, id):
        return RETRIEVE_URL_TEMPLATE.format(name=self.name, id=id)

    def __iter__(self):
        response = self.client.get(self.list_url(), self.params)
        data = response.json()
        objects = data[self.name]

        for obj in objects:
            yield obj


class PaginatedMixin(object):
    pages_next_key = 'next'

    def __iter__(self):
        response = self.client.get(self.list_url(), self.params)

        while response:
            data = response.json()
            objects = data[self.name]

            for obj in objects:
                yield obj

            try:
                next_url = data['pages'][self.pages_next_key]
            except KeyError:
                next_url = None

            response = self.client.get(next_url) if next_url else None


class ScrollableMixin(object):
    def scroll_url(self):
        return u'/'.join((self.list_url(), 'scroll'))

    def __iter__(self):
        url = self.scroll_url()
        params = self.params.copy()
        response = self.client.get(url, params)

        while response:
            data = response.json()

            if 'scroll_param' in data:
                params['scroll_param'] = data['scroll_param']
            else:
                raise TypeError(
                    '{} resource is not scrollable'
                    .format(type(self).__name__)
                )

            objects = data[self.name]

            for obj in objects:
                yield obj

            response = self.client.get(url, params) if objects else None


class WithNestedMixin(object):
    def __init__(self, *args, **kwargs):
        nested_classes = kwargs.pop('nested_classes', ())
        super(WithNestedMixin, self).__init__(*args, **kwargs)
        self.nested_classes = nested_classes

    def __iter__(self):
        for obj in super(WithNestedMixin, self).__iter__():
            for resource_cls in self.nested_classes:
                resource = resource_cls(self.client, obj)
                obj[resource.name] = list(resource)
            yield obj
