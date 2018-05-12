import pytest
import os
import sys
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from shutil import copy
import time

from click.testing import CliRunner

from pipenv_pipes.pipenv import PipedPopen
from pipenv_pipes.core import (
    find_environments,
    write_project_dir_project_file,
    resolve_envname_hash,
)


def touch(filename):
    try:
        os.utime(filename, None)
    except OSError:
        open(filename, 'a').close()


@pytest.fixture
def win_tempdir():
    # Default Temp dirs use windows short path:
    # 'C:\\Users\\GTALAR~1\\AppData'
    # The ~1 breaks --venv hash resolution,
    # so to ensure consitency will build the path manually
    if 'nt' not in os.name:
        return None
    path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp')
    assert '~' not in path
    assert os.path.exists(path)
    return path


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
def mock_projects_dir(project_names, win_tempdir):
    """ A folderpath with 2 sample project folders """
    with TemporaryDirectory(prefix='projects', dir=win_tempdir) as projects_dir:
        for project_name in project_names:
            os.makedirs(os.path.join(projects_dir, project_name))
        yield projects_dir


@pytest.fixture
def mock_env_home_empty(TempEnviron, mock_projects_dir):
    """
    A folderpath with 2 sample env folders (empty).
    Helful for fast tests that don't require an actual environment
    """
    with TemporaryDirectory(prefix='pipenv_home_fake') as pipenv_home:
        with TempEnviron(WORKON_HOME=pipenv_home):
            # TODO: Replace this with an actual pipenv fake env
            # that returns valid --venv so we can reduce usage
            # of mock_slow and run most tests witout an actual pipen install
            # https://github.com/pypa/pipenv/blob/master/pipenv/project.py#L223
            for project_name in os.listdir(mock_projects_dir):

                # Create Pipfile in Project File --venv checks for it
                project_dir = os.path.join(mock_projects_dir, project_name)
                pipfile = os.path.join(project_dir, 'Pipfile')
                with open(pipfile, 'w') as fp:
                    fp.write('')


                # Create a Fake Env folder
                hash_ = resolve_envname_hash(project_dir=project_dir)
                envname = '{}-{}'.format(project_name, hash_)
                envpath = os.path.join(pipenv_home, envname)
                python_fp = sys.executable
                if python_fp.endswith('exe'):
                    bin_path = os.path.join(envpath, 'Scripts')
                    activate = os.path.join(bin_path, 'activate.bat')
                else:
                    bin_path = os.path.join(envpath, 'bin')
                    activate = os.path.join(bin_path, 'activate')

                os.makedirs(envpath)
                os.makedirs(bin_path)
                touch(activate)
                copy(python_fp, bin_path, follow_symlinks=True)
                write_project_dir_project_file(envpath, project_dir)

            yield pipenv_home, mock_projects_dir
            # Sometimes python.exe is still budy, this give time to unlock
            time.sleep(0.)


@pytest.fixture
def mock_env_home_slow(TempEnviron, mock_projects_dir):
    with TemporaryDirectory(prefix='pipenv_home_real') as pipenv_home:
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


@pytest.fixture(name='environments')
def fake_environments():
    """ Used by unit.test_utils parametrics tests """
    from pipenv_pipes.core import Environment
    return [
        Environment(
            project_name='proj1',
            envname='proj1-1C_-wqgW',
            envpath='~/fakedir/proj1-12345678',
            binpath='~/fakedir/proj1-12345678/bin/python'
            ),
        Environment(
            project_name='proj2',
            envname='proj2-12345678',
            envpath='~/fakedir/proj2-12345678',
            binpath='~/fakedir/proj2-12345678/bin/python'
            ),
        Environment(
            project_name='abc-o',
            envname='abc-o-12345678',
            envpath='~/fakedir/abc-o-12345678',
            binpath='~/fakedir/abc-o-12345678/bin/python'
            ),
        Environment(
            project_name='notpipenv',
            envname='notpipenv',
            envpath='~/fakedir/notpipenv',
            binpath='~/fakedir/notpipenv/bin/python'
            ),
    ]
