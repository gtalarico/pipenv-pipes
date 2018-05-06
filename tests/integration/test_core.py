import pytest  # noqa: F401
import os
import time

from pipenv_pipes.core import (
    call_pipenv_venv,
    call_pipenv_shell,
    find_environments,
    read_project_dir_file,
    write_project_dir_project_file,
    delete_project_dir_file,
)


class TestRunPipesCli():

    def test_cli_run(self, runner, cli):
        """Test the CLI."""
        result = runner.invoke(cli.pipes)
        assert result.exit_code == 0

    def test_call_pipenv_venv_not_a_venv(self, test_dir):
        """ No virtual path has been created """
        path, error = call_pipenv_venv(test_dir)
        assert not path
        assert error

    def test_call_pipenv_shell(self, test_dir):
        proc, out, err = call_pipenv_shell(
            cwd=test_dir,
            timeout=15,
            pipe=True)
        # This passes with pytest -s
        # but fails without since pytest interferes with the stdout/stferr
        # Capturing
        # assert proc.returncode == -9
        assert "Use 'exit' to leave" in err

    def test_find_environments(self, runner):
        with runner.isolated_filesystem():
            os.makedirs('proj1-12345678')
            os.makedirs('proj2-12345678')
            environments = find_environments('.')
        assert len(environments) == 2
        assert 'proj1' in [e.project_name for e in environments]

    def test_find_environments_empty(self, test_dir):
        """ Environment could be empty """
        environments = find_environments(test_dir)
        assert len(environments) == 0


    def test_find_environments_does_not_exit(self):
        """ Invalid Folder. CLI Entry should catch, core func should fail """
        with pytest.raises(IOError):
            find_environments('/fakedir/')


class TestProjectDirFile():

    """ Test functions for managing the .project file, aka project_dir file """

    def test_write_project_dir_project_file(self, runner):
        envpath = '.'
        project_file = './.project'
        project_dir = 'fakeProjectPath'
        with runner.isolated_filesystem():
            write_project_dir_project_file(envpath=envpath,
                                           project_dir=project_dir)
            with open(project_file, 'r') as fp:
                assert fp.read() == project_dir

    def test_read_project_dir_file(self, runner):
        envpath = '.'
        project_file = './.project'
        with runner.isolated_filesystem():
            with open(project_file, 'w') as fp:
                fp.write('fakePath')
            assert read_project_dir_file(envpath) == 'fakePath'

    def test_delete_project_dir_file(self, runner):
        envpath = '.'
        project_file = './.project'
        with runner.isolated_filesystem():
            with open(project_file, 'w') as fp:
                fp.write('fakePath')
            assert os.path.exists(project_file)

            delete_project_dir_file(envpath)
            assert not os.path.exists(project_file)
