import pytest
import os
from contextlib import contextmanager
from tempfile import TemporaryDirectory

from click.testing import CliRunner

from pipenv_pipes.pipenv import PipedPopen
from pipenv_pipes.core import (
    find_environments,
    write_project_dir_project_file
)


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


@pytest.fixture
def temp_folder():
    """ A folderpath with for an empty folder """
    with TemporaryDirectory() as path:
        yield path


@pytest.fixture
def project_names():
    return [
        'proj1',
        'proj2'
    ]


@pytest.fixture()
def TempEnviron():
    """
    Context Manager Fixture for a controlled os.environ.
    Use kwargs to set desired variables.

    Usage:
        >>> with TempEnviron(WORKON_HOME=temp_fake_venvs_home):
        >>>    # do something
    """
    return _TempEnviron


@pytest.fixture
def mock_projects_dir(project_names):
    """ A folderpath with 2 sample project folders """
    with TemporaryDirectory(prefix='testprojects') as projects_dir:
        for project_name in project_names:
            os.makedirs(os.path.join(projects_dir, project_name))
        yield projects_dir


@pytest.fixture
def mock_env_home_empty(TempEnviron, mock_projects_dir):
    """
    A folderpath with 2 sample env folders (empty).
    Helful for fast tests that don't require an actual environment
    """
    with TemporaryDirectory(prefix='testenvs') as pipenv_home:
        with TempEnviron(WORKON_HOME=pipenv_home):
            # TODO: Replace this with an actual pipenv fake env
            # that returns valid --venv so we can reduce usage
            # of mock_slow and run most tests witout an actual pipen install
            # https://github.com/pypa/pipenv/blob/master/pipenv/project.py#L223
            for project_name in os.listdir(mock_projects_dir):
                envname = '{}-12345678'.format(project_name)
                os.makedirs(os.path.join(pipenv_home, envname))
            yield pipenv_home, mock_projects_dir


@pytest.fixture
def mock_env_home_slow(TempEnviron, mock_projects_dir):
    with TemporaryDirectory(prefix='envs') as pipenv_home:
        with TempEnviron(WORKON_HOME=pipenv_home):
            for project_name in os.listdir(mock_projects_dir):
                proj_dir = os.path.join(mock_projects_dir, project_name)
                output, code = PipedPopen(['pipenv', 'install'], cwd=proj_dir)
                assert code == 0
                # This fail on windows
                assert 'pipenv shell' in output

            # Make Project Links
            envs = find_environments(pipenv_home)
            for e in envs:
                project_dir = os.path.join(mock_projects_dir, e.project_name)
                write_project_dir_project_file(
                    envpath=e.envpath,
                    project_dir=project_dir
                )
            yield pipenv_home, mock_projects_dir


@pytest.fixture(name='runner')
def runner_fast(mock_env_home_empty):
    """ Runner Fast is used when a Real Env is not needed """
    runner = CliRunner()

    cwd = os.getcwd()
    pipenv_home, mock_projects_dir = mock_env_home_empty
    os.chdir(mock_projects_dir)  # Sets projects dir is cwd, for easier testing
    with runner.isolation():
        yield runner
    os.chdir(cwd)


@pytest.fixture
def runner_slow(mock_env_home_slow):
    """ Runner Slow is used when a Real Env - users mock_env_home """
    runner = CliRunner()

    cwd = os.getcwd()
    pipenv_home, mock_projects_dir = mock_env_home_slow
    os.chdir(mock_projects_dir)  # Sets projects dir is cwd, for easier testing
    with runner.isolation():
        yield runner
    os.chdir(cwd)
