#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `pipenv_pipes` cli."""

import pytest  # noqa: F401
import traceback
from pipenv_pipes.cli import pipes


#

def test_cli_help(runner):
    help_result = runner.invoke(pipes, args=['--help'])
    assert help_result.exit_code == 0
    assert 'show this message and exit' in help_result.output.lower()


def test_cli_version(runner):
    from pipenv_pipes import __version__
    result = runner.invoke(pipes, args=['--version'], catch_exceptions=False)
    assert result.exit_code == 0
    assert __version__ in result.output


def test_cli_from_shell():
    import subprocess
    result = subprocess.check_output(['pipes', '--help']).decode()
    assert 'show this message and exit' in result.lower()


@pytest.mark.curses
def test_cli_no_args(runner):
    result = runner.invoke(pipes)
    assert result.exit_code == 1
    assert 'query": ""' in result.output
    assert 'envs": 2' in result.output


@pytest.mark.skip('Not needed')
@pytest.mark.curses
def test_cli_no_args_verbose(runner):
    result = runner.invoke(
        pipes, ['--verbose'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'PIPENV_HOME' in result.output


@pytest.mark.curses
def test_many_match(runner):
    result = runner.invoke(pipes, args=['proj'])
    assert result.exit_code == 1
    assert 'query": "proj' in  result.output
    assert 'envs": 2' in result.output


def test_cli_list(runner):
    result = runner.invoke(
        pipes, args=['--list'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'proj1' in result.output


def test_cli_list_verbose(runner):
    result = runner.invoke(
        pipes, args=['--list', '--verbose'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'PIPENV_HOME' in result.output
    assert 'Python' in result.output


def test_no_match(runner):
    result = runner.invoke(
        pipes, args=['projxxx'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'no matches' in result.output.lower()


def test_one_match_do_shell(runner):
    result = runner.invoke(
        pipes, args=['proj1'], input='exit', catch_exceptions=False)
    assert result.exit_code == 0
    assert 'terminating pipes shell' in result.output.lower()


def test_one_match_unlink(runner):
    result = runner.invoke(
        pipes, args=['proj1', '--unlink'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'project directory cleared' in result.output.lower()


def test_one_match_no_link(runner):
    result = runner.invoke(
        pipes, args=['proj1', '--unlink'], catch_exceptions=False)
    assert result.exit_code == 0
    result = runner.invoke(pipes, args=['proj1', '--unlink'])
    assert result.exit_code == 0
    assert 'was already' in result.output.lower()
    result = runner.invoke(pipes, args=['proj1'])
    assert result.exit_code == 0
    # Message telling use he needs to create link
    assert 'pipes --link' in result.output


def test_do_link(runner):
    result = runner.invoke(
        pipes, args=['proj1', '--unlink'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'project directory cleared' in result.output.lower()

    result = runner.invoke(pipes, args=['--link', 'proj1'])
    assert result.exit_code == 0
    assert 'proj1' in result.output.lower()
    assert 'project directory set' in result.output.lower()


def test_do_link_no_assoc_env(runner, temp_folder):
    result = runner.invoke(
        pipes, args=['--link', temp_folder], catch_exceptions=False)
    assert result.exception
    assert 'looking for associated' in result.output.lower()
    assert 'no virtualenv has been created' in result.output.lower()


def test_completions(runner):
    result = runner.invoke(
        pipes, args=['--_completion'], catch_exceptions=False)
    assert result.exit_code == 0
    assert 'proj1' in result.output


class TestEnsureVars():
    """ Check for errors raised if Certain conditions are not met """

    def test_pipenv_home_no_envs(self, runner, temp_folder):
        """ WORKON_HOME exists but does not have any pipenv envs """
        env = dict(WORKON_HOME=temp_folder)
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
