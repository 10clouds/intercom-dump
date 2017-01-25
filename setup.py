#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click==6.7',
    'requests==2.13.0',
]

test_requirements = [
]

setup(
    name='intercom-dump',
    version='0.1.0',
    description="Python commandline application for dumping all intercom data to a sqlite database",
    long_description=readme + '\n\n' + history,
    author="Marek Skrajnowski",
    author_email='marek.skrajnowski@10clouds.com',
    url='https://github.com/mskrajnowski/intercom_dump',
    packages=[
        'intercom_dump',
    ],
    package_dir={'intercom_dump':
                 'intercom_dump'},
    entry_points={
        'console_scripts': [
            'intercom_dump=intercom_dump.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='intercom_dump',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
