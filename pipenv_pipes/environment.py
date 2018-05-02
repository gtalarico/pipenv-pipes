# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os


default_home = os.path.join(
    os.environ.get('XDG_DATA_HOME', '~/.local/share'), 'virtualenvs')

PIPENV_HOME = os.path.expanduser(os.getenv('WORKON_HOME', default_home))
PIPENV_ACTIVE = os.getenv('PIPENV_ACTIVE', 0) == '1'
PROMPT = os.getenv('PROMPT', '')
PIPENV_VENV_IN_PROJECT = os.getenv('PIPENV_VENV_IN_PROJECT')
VENV_IS_ACTIVE = os.getenv('VENV')
