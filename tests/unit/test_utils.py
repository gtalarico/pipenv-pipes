#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for `pipenv_pipes` utils module."""

import pytest
import os


from pipenv_pipes.utils import (
    get_project_name,
    get_query_matches,
    get_project_dir_filepath,
    get_index_from_query,
)


@pytest.mark.utils
@pytest.mark.parametrize("folder_name,expected", [
    ("nonpipenvproject", None),
    ("project1-1C_-wqgW", 'project1'),
    ("something-with-dash-awrasdQW", 'something-with-dash'),
])
def test_get_project_name(folder_name, expected):
    assert get_project_name(folder_name) == expected


@pytest.mark.utils
@pytest.mark.parametrize("query,num_results,envs", [
    ("proj", 2, pytest.lazy_fixture('environments')),
    ("proj1", 1, pytest.lazy_fixture('environments')),
    ("o", 4, pytest.lazy_fixture('environments')),
    ("zzz", 0, pytest.lazy_fixture('environments')),
])
def test_get_query_matches(query, num_results, envs):
    rv = get_query_matches(envs, query)
    assert len(rv) == num_results


def test_get_project_dir_filepath():
    path = os.path.join('fake', 'dir')
    expected = os.path.join(path, '.project')
    assert get_project_dir_filepath(path) == expected


@pytest.mark.utils
@pytest.mark.parametrize("query,expected_index", [
    ("1:", 1),
    ("54:", 54),
    ("123:23", None),
    ("a:", None),
    ("1", None),
])
def test_get_index_from_query(query, expected_index):
    assert get_index_from_query(query) == expected_index
