#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pipenv_pipes` package."""

import pytest

from click.testing import CliRunner

from pipenv_pipes import pipenv_pipes
from pipenv_pipes import cli


@pytest.fixture
def _fixture():
    pass


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pipenv_pipes.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
