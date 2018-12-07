#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import os

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',        # Required
    'colorama>=0.3',     # Note required, but nice as default
]

setup_requirements = [
    'pytest-runner'
    ]

test_requirements = [
    'click',
    'pytest',
    'pytest-lazy-fixture',
    'pytest-cov',
    ]

setup(
    name='pipenv_pipes',
    license="MIT license",
    keywords='pipenv_pipes',
    url='https://github.com/gtalarico/pipenv-pipes',
    version='0.7.1',
    author="Gui Talarico",
    author_email='gtalarico.dev@gmail.com',
    long_description=readme + '\n\n' + history,
    description="CLI Tool to help manage Pipenv Enviroments "
                "and corresponding Project Directories.",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'console_scripts': [
            'pipes=pipenv_pipes.cli:pipes',
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(
        include=[
            'pipenv_pipes',
            'pipenv_pipes.picker'
            ]),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
)
