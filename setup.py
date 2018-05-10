#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'colorama>=0.3',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', 'pytest-lazy-fixture', 'click']

setup(
    author="Gui Talarico",
    author_email='gui.talarico+pip@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        # "Programming Language :: Python :: 2",
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="CLI Tool to help manage Pipenv Enviroments "
                "and corresponding Project Directories.",
    entry_points={
        'console_scripts': [
            'pipes=pipenv_pipes.cli:pipes',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pipenv_pipes',
    name='pipenv_pipes',
    packages=find_packages(include=['pipenv_pipes']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gtalarico/pipenv-pipes',
    version='0.4.2-rc3',
    zip_safe=False,
)
