# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import re
from collections import namedtuple

Project = namedtuple('Project', ['name', 'envname', 'envpath'])


def get_project_name(folder_name):
    PIPENV_FOLDER_PAT = r'^(.+)-\w{8}$'
    match = re.search(PIPENV_FOLDER_PAT, folder_name)
    return None if not match else match.group(1)


def get_projects(pipenv_home):
    """Get Projects

    Args:
        pipenv_home (str): Absolute path of pipenv home folder

    Returns:
        (List[Project]): List of Projects
    """
    projects = []
    for folder_name in os.listdir(pipenv_home):
        folder_path = os.path.join(pipenv_home, folder_name)
        project_name = get_project_name(folder_name)
        if not project_name:
            continue
        project = Project(name=project_name,
                          envpath=folder_path,
                          envname=folder_name)
        projects.append(project)
    return projects


def get_matches(projects, query):
    matches = []
    for project in projects:
        if query.lower() in project.envname.lower():
            matches.append(project)
    return matches


def get_project_path_file(project_env_path):
    return os.path.join(project_env_path, '.project')


def get_project_dir(project):
    project_file = get_project_path_file(project.envpath)
    with open(project_file) as fp:
        return fp.read()


def set_project_dir(envpath, project_dir):
    project_file = get_project_path_file(envpath)
    with open(project_file, 'w') as fp:
        return fp.write(project_dir)
