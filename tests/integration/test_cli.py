#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `pipenv_pipes` cli."""

import pytest  # noqa: F401
import os


def test_cli_help(runner, cli):
    cli.ENVIRONMENTS = None
    help_result = runner.invoke(cli.pipes, args=['--help'])
    assert help_result.exit_code == 0
    assert 'show this message and exit' in help_result.output.lower()


def test_installed():
    import subprocess
    help_output = subprocess.check_output(['pipes', '--help']).decode()
    assert 'show this message and exit' in help_output.lower()


def test_one_match():
    pass


def test_no_match():
    pass


def test_many_match():
    pass


class TestEnsureVars():
    """ Check for errors raised if Certain conditions are not met """

    def test_pipenv_home_no_envs(self, runner, cli):
        with runner.isolated_filesystem():
            os.mkdir('fakedir')
            env = dict(WORKON_HOME='fakedir')
            result = runner.invoke(cli.pipes, env=env)
            assert result.exception
            assert 'no pipenv environments found' in result.output.lower()

    def test_pipenv_home(self, runner, cli):
        env = dict(WORKON_HOME='/fake/dir')
        result = runner.invoke(cli.pipes, env=env)
        assert result.exception
        assert 'could not find' in result.output.lower()

    def test_active_venv(self, runner, cli):
        env = dict(PIPENV_ACTIVE='1')
        result = runner.invoke(cli.pipes, env=env)
        assert result.exception
        assert 'shell is already active' in result.output.lower()

    def test_venv_is_active(self, runner, cli):
        env = dict(VENV='1')
        result = runner.invoke(cli.pipes, env=env)
        assert result.exception
        assert 'environment is already active' in result.output.lower()

    def test_pipenv_in_project(self, runner, cli):
        env = dict(PIPENV_VENV_IN_PROJECT='1')
        result = runner.invoke(cli.pipes, env=env)
        assert result.exception
        assert 'not supported' in result.output.lower()
