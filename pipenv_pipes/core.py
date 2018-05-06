
import os
import subprocess
from collections import namedtuple

from .utils import (
    get_project_name,
    get_project_dir_filepath
)

Environment = namedtuple('Environment', ['envpath', 'envname', 'project_name'])


def call_pipenv(*args, pipe=False, timeout=30, **kwargs):
    if pipe:
        kwargs.update(dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ))
    proc = subprocess.Popen(
        ['pipenv', *args],
        universal_newlines=True,  # Returns String instead of bytes
        **kwargs)
    try:
        output, err = proc.communicate(timeout=timeout)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        proc.kill()
        output, err = proc.communicate()
    else:
        pass
    finally:
        return proc, output, err


def call_pipenv_venv(project_dir, timeout=10):
    """ Calls ``pipenv --venv`` from a given project directory """
    proc, output, err = call_pipenv(
        '--venv',
        pipe=True,
        cwd=project_dir,
        timeout=timeout
    )
    return output.strip(), err.strip()


def call_pipenv_shell(cwd, envname='pipenv-shell', timeout=None, pipe=False):
    """ Calls ``pipenv shell``` from a given envname """
    environ = dict(os.environ)
    environ['PROMPT'] = '({}){}'.format(envname, os.getenv('PROMPT', ''))
    proc, output, err = call_pipenv(
        'shell',
        cwd=cwd,
        timeout=timeout,
        pipe=pipe,  # True For test only
        )
    return proc, output, err


def find_environments(pipenv_home):
    """
    Returns Environment NamedTuple created from list of folders found in the
    Pipenv Environment location
    """
    environments = []
    for folder_name in sorted(os.listdir(pipenv_home)):
        folder_path = os.path.join(pipenv_home, folder_name)
        project_name = get_project_name(folder_name)
        if not project_name:
            continue
        environment = Environment(project_name=project_name,
                                  envpath=folder_path,
                                  envname=folder_name)
        environments.append(environment)
    return environments


###############################
# Project Dir File (.project) #
###############################

def read_project_dir_file(envpath):
    project_file = get_project_dir_filepath(envpath)
    try:
        with open(project_file) as fp:
            return fp.read().strip()
    except IOError:
        return


def write_project_dir_project_file(envpath, project_dir):
    project_file = get_project_dir_filepath(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)


def delete_project_dir_file(envpath):
    project_file = get_project_dir_filepath(envpath)
    try:
        os.remove(project_file)
    except IOError:
        pass
    else:
        return project_file
