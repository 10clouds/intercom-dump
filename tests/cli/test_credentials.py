# -*- coding: utf-8 -*-

"""
test_credentials
----------------------------------

Checks whether intercom credentials are properly read from the commandline
arguments/environment.
"""

from click.testing import CliRunner
import pytest
import six

from intercom_dump import cli


# possible values for app id/api key and their validity
values = [
    # (value, is_valid)
    (None, False),
    ('', False),
    ('value', True),
]


def generate_args(option, env_key, values):
    """
    Builds all combinations of CliRunner.invoke() arguments for the given
    option and possible values.

    >>> from pprint import pprint
    >>> pprint(list(generate_args(
    ...     '--option',
    ...     'ENV_VAR',
    ...     [(None, False), ('some', True)],
    ... )))
    [{'is_valid': False},
     {'args': ['--option', 'some'], 'is_valid': True},
     {'env': {'ENV_VAR': 'some'}, 'is_valid': True}]
    """

    for value, is_valid in values:
        if value is None:
            yield dict(is_valid=is_valid)
        else:
            yield dict(args=[option, value], is_valid=is_valid)
            yield dict(env={env_key: value}, is_valid=is_valid)


def merge_args(*args_list):
    """
    Merges CliRunner.invoke() arguments.

    >>> from pprint import pprint
    >>> pprint(merge_args(
    ...     {'args': ['--option', 'some'], 'env': {'OPTION': 'some'}},
    ...     {'env': {'OTHER': ''}, 'is_valid': False},
    ...     {'args': ['--other'], 'is_valid': False},
    ... ))
    {'args': ['--option', 'some', '--other'],
     'env': {'OPTION': 'some', 'OTHER': ''},
     'is_valid': False}
    """

    merged = dict(args=[], env={}, is_valid=True)

    for args in args_list:
        merged['args'].extend(args.get('args', []))
        merged['env'].update(args.get('env', {}))
        merged['is_valid'] = merged['is_valid'] and args.get('is_valid', True)

    return merged


def raw_args(args):
    """
    Removes the is_valid flag from an args dict
    """

    args = args.copy()
    args.pop('is_valid', None)
    return args


def args_str(args):
    """
    Returns a user-friendly representation of CliRunner.invoke() arguments.

    >>> args_str(dict(args=['--option', 'value'], env={'ENV_VAR': 'value'}))
    u"ENV_VAR='value' intercom_dump --option 'value'"
    """

    parts = []

    parts.extend(
        u'{}={}'.format(key, repr(value))
        for key, value in six.iteritems(args['env'])
    )
    parts.append('intercom_dump')
    parts.extend(
        arg if arg.startswith('--') else repr(arg)
        for arg in args['args']
    )

    return u' '.join(parts)


invoke_args = [
    merge_args(app_id_args, api_key_args)
    for app_id_args in generate_args('--app-id', 'INTERCOM_APP_ID', values)
    for api_key_args in generate_args('--api-key', 'INTERCOM_API_KEY', values)
]


valid_args = [
    raw_args(args)
    for args in invoke_args
    if args['is_valid']
]


invalid_args = [
    raw_args(args)
    for args in invoke_args
    if not args['is_valid']
]


@pytest.mark.parametrize('args', invalid_args, ids=args_str)
def test_invalid(args):
    runner = CliRunner()
    result = runner.invoke(cli.main, **args)
    assert result.exit_code != 0
    assert 'You must specify intercom app id and api key' in result.output


@pytest.mark.parametrize('args', valid_args, ids=args_str)
def test_valid(args):
    runner = CliRunner()
    result = runner.invoke(cli.main, **args)
    assert result.exit_code == 0
