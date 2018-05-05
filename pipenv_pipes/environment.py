# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os


class EnvVars():

    def __init__(self):
        # Class Storate Allows Variables to be Reinitialized / Reset
        # as needed. Especially helpful for tests
        _ENV_DEFAULT_HOME = os.path.join(
            os.environ.get('XDG_DATA_HOME', '~/.local/share'), 'virtualenvs')

        self.PIPENV_HOME = os.path.expanduser(
            os.getenv('WORKON_HOME', _ENV_DEFAULT_HOME))

        self.PIPENV_IS_ACTIVE = os.getenv('PIPENV_ACTIVE', '')
        self.PIPENV_VENV_IN_PROJECT = os.getenv('PIPENV_VENV_IN_PROJECT', '')
        self.VENV_IS_ACTIVE = os.getenv('VENV', '')
