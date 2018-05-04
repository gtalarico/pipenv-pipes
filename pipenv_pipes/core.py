
import os
import subprocess
from collections import namedtuple

from .environment import PROMPT
from .utils import (
    get_project_name,
    get_project_dir_filepath
)

Environment = namedtuple('Environment', ['project_name', 'envname', 'envpath'])


def call_pipenv_venv(project_dir):
    """ Calls ``pipenv --venv`` from a given project directory """
    try:
        output = subprocess.check_output(['pipenv', '--venv'], cwd=project_dir)
    except subprocess.CalledProcessError as exc:
        pass
    else:
        return output.decode().strip()


def call_pipenv_shell(project_dir, envname):
    """ Calls ``pipenv shell``` from a given envname """
    env_vars = os.environ.copy()
    env_vars['PROMPT'] = '({}){}'.format(envname, PROMPT)
    return subprocess.call(['pipenv', 'shell'], cwd=project_dir, env=env_vars)


def find_environments(pipenv_home):
    """
    Returns Environment Objects created from list of folders found in the
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

def read_project_dir_file(project):
    # Move to Core
    project_file = get_project_dir_filepath(project.envpath)
    try:
        with open(project_file) as fp:
            return fp.read().strip()
    except IOError:
        return


def write_project_dir_project_file(envpath, project_dir):
    # Move to Core
    project_file = get_project_dir_filepath(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)


def delete_project_dir_file(envpath):
    # Move to Core
    project_file = get_project_dir_filepath(envpath)
    try:
        os.remove(project_file)
    except IOError:
        pass
    else:
        return project_file

