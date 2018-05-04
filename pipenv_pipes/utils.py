# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import re
from collections import namedtuple
import subprocess

from .environment import PROMPT

Environment = namedtuple('Environment', ['project_name', 'envname', 'envpath'])


def get_env_name(folder_name):
    PIPENV_FOLDER_PAT = r'^(.+)-\w{8}$'
    match = re.search(PIPENV_FOLDER_PAT, folder_name)
    return None if not match else match.group(1)


def get_environments(pipenv_home):
    # Move to Core
    """Get Projects

    Args:
        pipenv_home (str): Absolute path of pipenv home folder

    Returns:
        (List[Environment]): List of Environments Tuples
    """
    environments = []
    for folder_name in sorted(os.listdir(pipenv_home)):
        folder_path = os.path.join(pipenv_home, folder_name)
        project_name = get_env_name(folder_name)
        if not project_name:
            continue
        environment = Environment(project_name=project_name,
                                  envpath=folder_path,
                                  envname=folder_name)
        environments.append(environment)
    return environments


def get_matches(environments, query):
    matches = []
    for environment in environments:
        if query.lower() in environment.envname.lower():
            matches.append(environment)
    return matches


def get_project_path_file(envpath):
    return os.path.join(envpath, '.project')


def get_project_dir(project):
    # Move to Core
    project_file = get_project_path_file(project.envpath)
    try:
        with open(project_file) as fp:
            return fp.read().strip()
    except IOError:
        return


def set_project_dir_project_file(envpath, project_dir):
    # Move to Core
    project_file = get_project_path_file(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)


def get_envname_index(query):
    """ Index should be passed as 1: """
    pat = r'(\d+):$'
    match = re.match(pat, query)
    return None if not match else int(match.group(1))


def unset_project_dir(envpath):
    # Move to Core
    project_file = get_project_path_file(envpath)
    try:
        os.remove(project_file)
    except IOError:
        pass
    else:
        return project_file

def get_env_path_from_project_dir(project_dir):
    # Move to Core
    try:
        output = subprocess.check_output(['pipenv', '--venv'], cwd=project_dir)
    except subprocess.CalledProcessError as exc:
        pass
    else:
        return output.decode().strip()

def start_pipenv_shell(project_dir, envname):
    # Move to Core
    env_vars = os.environ.copy()
    env_vars['PROMPT'] = '({}){}'.format(envname, PROMPT)
    out = subprocess.call(['pipenv', 'shell'], cwd=project_dir, env=env_vars)
