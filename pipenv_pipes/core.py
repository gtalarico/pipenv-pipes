
import os
import subprocess
from collections import namedtuple

from .utils import (
    get_project_name,
    get_project_dir_filepath
)

Environment = namedtuple('Environment', ['envpath', 'envname', 'project_name'])


def call_pipenv_venv(project_dir):
    """ Calls ``pipenv --venv`` from a given project directory """
    try:
        proc = subprocess.Popen(
            ['pipenv', '--venv'], cwd=project_dir, stdout=subprocess.PIPE)
        output, err = proc.communicate(timeout=15)
    except subprocess.CalledProcessError as exc:
        raise
    else:
        return output.decode().strip()
    finally:
        proc.kill()


def call_pipenv_shell(project_dir, envname):
    """ Calls ``pipenv shell``` from a given envname """
    environ = dict(os.environ)
    environ['PROMPT'] = '({}){}'.format(envname, os.getenv('PROMPT', ''))
    proc = subprocess.Popen(['pipenv', 'shell'], cwd=project_dir, env=environ)
    # proc = subprocess.call(['pipenv', 'shell'], cwd=project_dir, env=environ)
    proc.communicate()
    return proc


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
