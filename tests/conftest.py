import pytest
import os
from subprocess import Popen, PIPE
from contextlib import contextmanager
from tempfile import TemporaryDirectory
import shutil
import tarfile
from click.testing import CliRunner

from pipenv.project import Project

from pipenv_pipes.core import (
    find_environments,
    write_project_dir_project_file,
)
from pipenv_pipes.environment import EnvVars

HERE = os.path.dirname(__file__)


def touch(filename):
    try:
        os.utime(filename, None)
    except OSError:
        open(filename, 'a').close()


def unzip_tar(src, dst):
    with tarfile.open(src, "r:gz") as tar:
        tar.extractall(path=dst)


@pytest.fixture
def env_vars():
    return EnvVars()


@pytest.fixture(scope='session')
def venv_fresh():
    with TemporaryDirectory() as folder:
        venv_cmd = 'virtualenv --no-pip --no-wheel --no-setuptools'
        cmd = '{} {}'.format(venv_cmd, folder)
        proc = Popen(cmd.split(' '), stderr=PIPE, stdout=PIPE)
        out, err = proc.communicate()
        if err:
            raise Exception(err)
        yield folder


@pytest.fixture
def win_tempdir(env_vars):
    # Default %TEMP% returns windows short path (C:\\Users\\GTALAR~1\\AppData)
    # The`~1`` breaks --venv hash resolution, so we must build path manually
    # On other systems this will be none, so default env will be used
    if not env_vars.IS_WINDOWS:
        return None
    path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp')
    assert '~' not in path
    assert os.path.exists(path)
    return path


@pytest.fixture
def temp_folder():
    """ A folderpath with for an empty folder """
    with TemporaryDirectory() as path:
        yield path


@pytest.fixture
def project_names():
    return ['proj1', 'proj2']


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
def TempEnviron():
    """
    >>> with TempEnviron(WORKON_HOME=temp_fake_venvs_home):
    >>>    # do something
    """
    return _TempEnviron


@pytest.fixture
def mock_projects_dir(project_names, win_tempdir):
    """ A folderpath with 2 sample project folders """
    with TemporaryDirectory(
            prefix='projects', dir=win_tempdir) as projects_dir:
        for project_name in project_names:
            os.makedirs(os.path.join(projects_dir, project_name))
        yield projects_dir


@pytest.fixture
def mock_env_home(TempEnviron, mock_projects_dir, venv_fresh):
    __cwd = os.getcwd()
    with TemporaryDirectory(prefix='pipenv_home_real') as pipenv_home:

        project_names = os.listdir(mock_projects_dir)
        for project_name in project_names:
            project_dir = os.path.join(mock_projects_dir, project_name)
            pipfile = os.path.join(project_dir, 'Pipfile')
            touch(pipfile)

            os.chdir(project_dir)
            with TempEnviron(WORKON_HOME=pipenv_home):
                project = Project()
                envname = project.virtualenv_name
            os.chdir(__cwd)

            envpath = os.path.join(pipenv_home, envname)
            shutil.copytree(venv_fresh, envpath)

        # Make Project Links
        envs = find_environments(pipenv_home)
        for e in envs:
            project_dir = os.path.join(mock_projects_dir, e.project_name)
            write_project_dir_project_file(
                envpath=e.envpath,
                project_dir=project_dir
            )
        with TempEnviron(WORKON_HOME=pipenv_home):
            yield pipenv_home, mock_projects_dir
        os.chdir(__cwd)


@pytest.fixture(name='runner')
def runner_fast(mock_env_home):
    runner = CliRunner()
    cwd = os.getcwd()
    pipenv_home, mock_projects_dir = mock_env_home
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
