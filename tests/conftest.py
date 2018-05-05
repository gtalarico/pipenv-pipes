import pytest
import os
from imp import reload

from click.testing import CliRunner


@pytest.fixture(autouse=True)
def clean_environment():
    BAD_VARS = [
        'PIPENV_ACTIVE',
        'PIPENV_VENV_IN_PROJECT',
        'VENV',
        'VIRTUAL_ENV'
    ]
    old_environ = dict(os.environ)
    [os.environ.pop(k, None) for k in BAD_VARS]

    yield dict(os.environ)
    os.environ.update(old_environ)


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


@pytest.fixture()
def cli(clean_environment):
    from pipenv_pipes import cli, environment
    yield cli
    reload(environment)
    reload(cli)


@pytest.fixture
def runner():
    runner = CliRunner()
    with runner.isolation():
        yield runner
