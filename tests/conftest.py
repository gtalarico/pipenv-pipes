import pytest
import os
from imp import reload
from contextlib import contextmanager

from click.testing import CliRunner


@pytest.fixture
def environments():
    """ Used by unit.test_utils parametrics tests """
    from pipenv_pipes.core import Environment
    return [
        Environment('proj1', 'proj1-12345678', '~/fakedir/proj1-12345678'),
        Environment('proj2', 'proj2-12345678', '~/fakedir/proj2-12345678'),
        Environment('abc-o', 'abc-o-12345678', '~/fakedir/abc-o-12345678'),
        Environment('notpipenv', 'notpipenv', '~/fakedir/notpipenv'),
    ]


@contextmanager
def _temp_environ():
    RELEVANT_VARS = dict(
        PIPENV_ACTIVE='',
        PIPENV_VENV_IN_PROJECT='',
        VENV='',
        VIRTUAL_ENV=''
    )
    old_environ = dict(os.environ)
    os.environ.update(RELEVANT_VARS)
    yield
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture(autouse=True)
def temp_environ():
    return _temp_environ


@pytest.fixture()
def cli(temp_environ):
    with temp_environ():
        from pipenv_pipes import cli, environment
        yield cli
        reload(environment)
        reload(cli)


@pytest.fixture
def runner():
    runner = CliRunner()
    with runner.isolation():
        yield runner
