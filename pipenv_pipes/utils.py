# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import re
from collections import namedtuple
import subprocess

Environment = namedtuple('Environment', ['project_name', 'envname', 'envpath'])


def get_env_name(folder_name):
    PIPENV_FOLDER_PAT = r'^(.+)-\w{8}$'
    match = re.search(PIPENV_FOLDER_PAT, folder_name)
    return None if not match else match.group(1)


def get_environments(pipenv_home):
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


def get_matches(projects, query):
    matches = []
    for project in projects:
        if query.lower() in project.envname.lower():
            matches.append(project)
    return matches


def get_project_path_file(envpath):
    return os.path.join(envpath, '.project')


def get_project_dir(project):
    project_file = get_project_path_file(project.envpath)
    try:
        with open(project_file) as fp:
            return fp.read().strip()
    except IOError:
        return


def set_project_dir_project_file(envpath, project_dir):
    project_file = get_project_path_file(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)


def get_envname_index(query):
    """ Index should be passed as 1: """
    pat = r'(\d+):$'
    match = re.match(pat, query)
    return None if not match else int(match.group(1))


def unset_project_dir(envpath):
    project_file = get_project_path_file(envpath)
    try:
        os.remove(project_file)
    except IOError:
        pass
    else:
        return project_file

def get_env_path_from_project_dir(project_dir):
    try:
        output = subprocess.check_output(['pipenv', '--venv'], cwd=project_dir)
    except subprocess.CalledProcessError as exc:
        pass
    else:
        return output.decode().strip()
