import collections
import functools
import itertools


def iter_data(data, name):
    return (obj for obj in data[name])


def iter_resource(client, name, params=None):
    url = client.build_url(name)
    data = client.get(url, params).json()
    return iter_data(data, name)


def iter_pages(client, name, params=None, next_key='next_url'):
    url = client.build_url(name)

    while url:
        data = client.get(url, params).json()
        yield data

        try:
            url = data['pages'][next_key]
            params = None
        except KeyError:
            url = None


def iter_paginated_resource(client, name, params=None, next_key='next_url'):
    for page in iter_pages(client, name, params, next_key):
        for obj in iter_data(page, name):
            yield obj


registry = {}


def register(name=None):
    def decorator(fun):
        registry[name or fun.__name__] = fun
        return fun

    return decorator


def build_resource(name, paginated=True, register=True):
    if paginated:
        def resource(client):
            return iter_paginated_resource(client, name)
    else:
        def resource(client):
            return iter_resource(client, name)

    if register:
        registry_name = register if isinstance(register, basestring) else name
        registry[registry_name] = resource

    resource.__name__ = name
    return resource


def decorate_with_resource(parent, child, key):
    @functools.wraps(parent)
    def wrapper(client, *args):
        for obj in parent(client, *args):
            child_args = args + (obj,)
            child_value = child(client, *child_args)
            obj[key] = (
                list(child_value)
                if isinstance(child_value, collections.Iterator)
                else child_value
            )
            yield obj

    return wrapper


def prepare_resources(client, resource_names):
    resource_names = sorted(resource_names)
    resources_by_name = {}
    roots = set()

    for name in resource_names:
        resource = registry.get(name)
        parent_name, _, parent_key = name.rpartition('.')

        if parent_name:
            resources_by_name[parent_name] = decorate_with_resource(
                resources_by_name[parent_name],
                resource,
                parent_key,
            )
        else:
            resources_by_name[name] = resource
            roots.add(name)

    return [resources_by_name[name](client) for name in roots]


def iter_objects(client, resource_names):
    return itertools.chain.from_iterable(
        prepare_resources(client, resource_names),
    )
