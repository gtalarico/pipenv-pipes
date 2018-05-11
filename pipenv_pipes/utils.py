# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import re
import pathlib
import hashlib
import base64

from .environment import EnvVars


def get_project_name(folder_name):
    """ Returns name of a project given a Pipenv Environment folder """
    PIPENV_FOLDER_PAT = r'^(.+)-[\w_-]{8}$'
    match = re.search(PIPENV_FOLDER_PAT, folder_name)
    return None if not match else match.group(1)


def get_query_matches(environments, query):
    """ Returns matching environments from an Environment list and a query """
    matches = []
    for environment in environments:
        if query.lower() in environment.envname.lower():
            matches.append(environment)
    return matches


def get_project_dir_filepath(envpath):
    """ Returns .project filepath from an environment path """
    return os.path.join(envpath, '.project')


def get_index_from_query(query):
    """ Index should be passed as 1: """
    pat = r'(\d+):$'
    match = re.match(pat, query)
    return None if not match else int(match.group(1))


def collapse_path(path):
    """ Replaces Home and WorkOn values in a path for their variable names """
    envvars = EnvVars()
    workon = envvars.PIPENV_HOME
    if not envvars.IS_WINDOWS:
        home = os.environ['HOME']
    else:
        home = os.environ['USERPROFILE']
    path = path.replace(workon, '$PIPENV_HOME')
    path = path.replace(home, '~')
    return path


def resolve_envname(project_dir):
    """
    Attempts to resolve envname.
    Although this might not be reliable, currently the only alternative
    is to from project_dir run `pipenv --venv`. This is slow for use
    and testing. Initially this is intended to be used for testing only,
    however if it remains stable it could replace the call_pipenv_venv calls
    """
    pipfile = pathlib.PurePath(project_dir) / 'Pipfile'
    hash = hashlib.sha256(str(pipfile).encode()).digest()[:6]
    encoded_hash = base64.urlsafe_b64encode(hash).decode()
    return encoded_hash[:8]
