import pytest
import os
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from click.testing import CliRunner


@contextmanager
def _TempEnviron(**env):
    old_environ = dict(os.environ)
    os.environ.pop('PIPENV_ACTIVE', None)
    os.environ.pop('PIPENV_VENV_IN_PROJECT', None)
    os.environ.pop('VENV', None)
    os.environ.pop('VIRTUAL_ENV', None)
    os.environ.update(env)
    yield
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture()
def TempEnviron():
    return _TempEnviron



@pytest.fixture
def temp_empty():
    with TemporaryDirectory() as path:
        yield path


@pytest.fixture
def temp_fake_projects_dir():
    with TemporaryDirectory(prefix='testprojects') as path:
        os.makedirs(os.path.join(path, 'proj1'))
        os.makedirs(os.path.join(path, 'proj2'))
        yield path



@pytest.fixture
def temp_fake_venvs_home():
    with TemporaryDirectory(prefix='testenvs') as path:
        os.makedirs(os.path.join(path, 'proj1-12345678'))
        os.makedirs(os.path.join(path, 'proj2-23456789'))
        yield path


@pytest.fixture
def runner(TempEnviron, temp_fake_venvs_home, temp_fake_projects_dir):
    runner = CliRunner()
    with runner.isolation():
        with TempEnviron(WORKON_HOME=temp_fake_venvs_home):
            yield runner
