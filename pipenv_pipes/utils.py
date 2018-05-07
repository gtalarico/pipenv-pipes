# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import re


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
