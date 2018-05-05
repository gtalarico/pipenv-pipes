#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `pipenv_pipes` cli."""

import pytest  # noqa: F401


def test_cli_help(runner, cli):
    cli.ENVIRONMENTS = None
    help_result = runner.invoke(cli.pipes, args=['--help'])
    assert help_result.exit_code == 0
    assert 'show this message and exit' in help_result.output.lower()


def test_installed():
    import subprocess
    help_output = subprocess.check_output(['pipes', '--help']).decode()
    assert 'show this message and exit' in help_output.lower()


class TestEnsureVars():
    """ Check for errors raised if Certain conditions are not met """

    def test_not_pipenv_found(self, runner, cli):
        cli.ENVIRONMENTS = []
        result = runner.invoke(cli.pipes)
        assert result.exception
        assert 'no pipenv environments found' in result.output.lower()

    def test_pipenv_home(self, runner, cli):
        cli.PIPENV_HOME = '/fake/dir'
        result = runner.invoke(cli.pipes)
        assert result.exception
        assert 'could not find' in result.output.lower()

    def test_active_venv(self, runner, cli):
        cli.PIPENV_ACTIVE = '1'
        result = runner.invoke(cli.pipes)
        assert result.exception
        assert 'shell is already active' in result.output.lower()

    def test_venv_is_Active(self, runner, cli):
        cli.VENV_IS_ACTIVE = '1'
        result = runner.invoke(cli.pipes)
        assert result.exception
        assert 'environment is already active' in result.output.lower()

    def test_pipenv_in_project(self, runner, cli):
        cli.PIPENV_VENV_IN_PROJECT = '1'
        result = runner.invoke(cli.pipes)
        assert result.exception
        assert 'not supported' in result.output.lower()
