#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `pipenv_pipes` cli."""

import pytest

from click.testing import CliRunner


@pytest.fixture
def runner():
    runner = CliRunner()
    with runner.isolation():
        yield runner


class TestRunPipesCli():

    def test_cli_run(self, runner, cli):
        """Test the CLI."""
        result = runner.invoke(cli.pipes)
        assert result.exit_code == 0

    def test_cli_help(self, runner, cli):
        help_result = runner.invoke(cli.pipes, args=['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_invalid_index(self, runner, cli):
        result = runner.invoke(cli.pipes, args=['999999999999:'])
        assert result.exception
        assert 'invalid' in result.output.lower()


class TestEnsureVars():

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

    def test_pipenv_in_project(self, runner, cli):
        cli.PIPENV_VENV_IN_PROJECT = '1'
        result = runner.invoke(cli.pipes)
        assert result.exception
        assert 'not supported' in result.output.lower()
