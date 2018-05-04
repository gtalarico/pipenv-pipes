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


def test_cli_run(runner, cli):
    """Test the CLI."""
    result = runner.invoke(cli.pipes)
    assert result.exit_code == 0


def test_cli_help(runner, cli):
    help_result = runner.invoke(cli.pipes, args=['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


def test_invalid_index(runner, cli):
    result = runner.invoke(cli.pipes, args=['999999999999:'])
    assert result.exception
    assert 'invalid' in result.output.lower()


def test_active_venv(runner, cli):
    cli.PIPENV_ACTIVE = '1'
    result = runner.invoke(cli.pipes)
    assert result.exception
    assert 'already active' in result.output.lower()


# def test_project_dir_file(runner, cli):
    # with runner.isolated_filesystem():
#    with open('hello.txt', 'w') as f:
#         f.write('Hello World!')
