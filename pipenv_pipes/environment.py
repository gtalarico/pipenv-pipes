# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import sys


class EnvVars():

    def __init__(self):
        self.IS_WINDOWS = sys.platform == 'win32'
        self.IS_MAC = sys.platform == 'darwin'
        self.IS_LINUX = sys.platform == 'linux'

        if self.IS_WINDOWS:
            default_home = '~/.virtualenvs'
        else:
            default_home = os.path.join(
                os.environ.get('XDG_DATA_HOME', '~/.local/share'),
                'virtualenvs')

        self.PIPENV_HOME = os.path.expanduser(
            os.getenv('WORKON_HOME', default_home))

        self.PIPENV_IS_ACTIVE = os.getenv('PIPENV_ACTIVE', '')
        self.PIPENV_VENV_IN_PROJECT = os.getenv('PIPENV_VENV_IN_PROJECT', '')
        self.VENV_IS_ACTIVE = os.getenv('VENV', '')

        try:
            import curses  # noqa flake8
        except ImportError:
            self.HAS_CURSES = False
        else:
            self.HAS_CURSES = True

    def validate_environment(self):

        if not os.path.exists(self.PIPENV_HOME):
            error = (
                'Could not find Pipenv Environments location. [{}] \n'
                'If you are using a non-default location you will need to '
                'add the path to $WORKON_HOME.'.format(self.PIPENV_HOME))

        elif self.PIPENV_IS_ACTIVE:
            error = (
                "Pipenv Shell is already active. \n"
                "Use 'exit' to close the shell before starting a new one.")

        elif self.VENV_IS_ACTIVE:
            error = (
                "A Virtual environment is already active.\n"
                "Use 'deactivate' to close disable the enviroment "
                "before starting a new one.")

        elif self.PIPENV_VENV_IN_PROJECT:
            error = 'PIPENV_VENV_IN_PROJECT is not supported at this time'

        else:
            return

        return error
