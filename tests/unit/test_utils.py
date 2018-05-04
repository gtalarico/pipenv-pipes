import pytest
import os

from pipenv_pipes.utils import (
    get_env_name,
    Environment,
    get_matches,
    get_project_path_file,
    get_envname_index,

)


@pytest.fixture
def environments():
    return [
        Environment('proj1', 'proj1-12345678', '~/fakedir/proj1-12345678'),
        Environment('proj2', 'proj2-12345678', '~/fakedir/proj2-12345678'),
        Environment('abc-o', 'abc-o-12345678', '~/fakedir/abc-o-12345678'),
        Environment('notpipenv', 'notpipenv', '~/fakedir/notpipenv'),
    ]


@pytest.mark.utils
@pytest.mark.parametrize("folder_name,expected", [
    ("nonpipenvproject", None),
    ("project1-12345678", 'project1'),
    ("something-with-dash-awrasdQW", 'something-with-dash'),
])
def test_get_env_name(folder_name, expected):
    assert get_env_name(folder_name) == expected


@pytest.mark.utils
@pytest.mark.parametrize("query,num_results,envs", [
    ("proj", 2, pytest.lazy_fixture('environments')),
    ("proj1", 1, pytest.lazy_fixture('environments')),
    ("o", 4, pytest.lazy_fixture('environments')),
    ("zzz", 0, pytest.lazy_fixture('environments')),
])
def test_get_matches(query, num_results, envs):
    rv = get_matches(envs, query)
    assert len(rv) == num_results


def test_get_project_path_file():
    path = os.path.join('fake', 'dir')
    expected = os.path.join(path, '.project')
    assert get_project_path_file(path) == expected


@pytest.mark.utils
@pytest.mark.parametrize("query,expected_index", [
    ("1:", 1),
    ("54:", 54),
    ("123:23", None),
    ("a:", None),
    ("1", None),
])
def test_get_envname_index(query, expected_index):
    assert get_envname_index(query) == expected_index
