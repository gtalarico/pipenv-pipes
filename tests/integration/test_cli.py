#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `pipenv_pipes` cli."""

import pytest  # noqa: F401
import os

from pipenv_pipes.cli import pipes


def test_cli_help(runner):
    help_result = runner.invoke(pipes, args=['--help'])
    assert help_result.exit_code == 0
    assert 'show this message and exit' in help_result.output.lower()


def test_installed():
    import subprocess
    help_output = subprocess.check_output(['pipes', '--help']).decode()
    assert 'show this message and exit' in help_output.lower()


@pytest.mark.skip
def test_no_args(runner):
    pass


@pytest.mark.skip
def test_one_match():
    pass


@pytest.mark.skip
def test_no_match():
    pass


@pytest.mark.skip
def test_many_match():
    pass


class TestEnsureVars():
    """ Check for errors raised if Certain conditions are not met """

    def test_pipenv_home_no_envs(self, runner, temp_empty):
        """ WORKON_HOME exists but does not have any pipenv envs """
        env = dict(WORKON_HOME=temp_empty)
        result = runner.invoke(pipes, env=env)
        assert result.exception
        assert 'no pipenv environments found' in result.output.lower()

    def test_pipenv_home_not_exists(self, runner):
        """ WORKON_HOME is an invalid dir """
        env = dict(WORKON_HOME='/fake/dir')
        result = runner.invoke(pipes, env=env)
        assert result.exception
        assert 'could not find' in result.output.lower()

    def test_active_venv(self, runner):
        """ Early exit when a pipenv shell is already active """
        env = dict(PIPENV_ACTIVE='1')
        result = runner.invoke(pipes, env=env)
        assert result.exception
        assert 'shell is already active' in result.output.lower()

    def test_venv_is_active(self, runner):
        """ Early exit when a virtualenv is already active """
        env = dict(VENV='1')
        result = runner.invoke(pipes, env=env)
        assert result.exception
        assert 'environment is already active' in result.output.lower()

    def test_pipenv_in_project(self, runner):
        """ Early return if using VEN_IN_PROJECT """
        env = dict(PIPENV_VENV_IN_PROJECT='1')
        result = runner.invoke(pipes, env=env)
        assert result.exception
        assert 'not supported' in result.output.lower()
