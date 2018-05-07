""" Test Core Functions """

import pytest  # noqa: F401
import os
from os.path import join

from pipenv_pipes.core import (
    find_environments,
    read_project_dir_file,
    write_project_dir_project_file,
    delete_project_dir_file,
)


class TestFindEnvironments():

    def test_find_environments(self, mock_env_home_empty):
        pipenv_home, mock_projects_dir = mock_env_home_empty
        # Add a non env to mock projects ensure it's not picked up
        os.makedirs(os.path.join(pipenv_home, 'notanenv'))

        environments = find_environments(pipenv_home)
        assert len(environments) == 2
        assert 'proj1' in [e.project_name for e in environments]

    def test_find_environments_empty(self, temp_folder):
        """ Environment could be empty """
        environments = find_environments(temp_folder)
        assert len(environments) == 0

    def test_find_environments_does_not_exit(self):
        """ Invalid Folder. CLI Entry should catch, core func should fail """
        with pytest.raises(IOError):
            find_environments('/fakedir/')


class TestProjectDirFile():

    """ Test functions for managing the .project file, aka project_dir file """

    def test_write_project_dir_project_file(self, temp_folder):
        project_file = join(temp_folder, '.project')
        project_dir = 'fakeProjectPath'
        write_project_dir_project_file(
            envpath=temp_folder,
            project_dir=project_dir)
        with open(project_file, 'r') as fp:
            assert fp.read() == project_dir

    def test_read_project_dir_file(self, temp_folder):
        project_file = join(temp_folder, '.project')
        with open(project_file, 'w') as fp:
            fp.write('fakePath')
        assert read_project_dir_file(temp_folder) == 'fakePath'

    def test_delete_project_dir_file(self, temp_folder):
        project_file = join(temp_folder, '.project')

        with open(project_file, 'w') as fp:
            fp.write('fakePath')
        delete_project_dir_file(temp_folder)
        assert not os.path.exists(project_file)
