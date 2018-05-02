#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pipenv_pipes` package."""

import pytest

from click.testing import CliRunner
from pipenv_pipes import cli
from pipenv_pipes import utils


@pytest.fixture
def _fixture():
    pass


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.pipes)
    assert result.exit_code == 0
    assert 'Pipenv Environments' in result.output
    help_result = runner.invoke(cli.pipes, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
