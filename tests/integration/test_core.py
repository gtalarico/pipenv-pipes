import pytest  # noqa: F401
import os

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

    # def test_call_pipenv_venv(self, runner, cli):
        # with runner.isolated_filesystem():
            # out = call_pipenv_venv('fakedir', 'CustomPrompt')
            # import pdb; pdb.set_trace()

    # def test_call_pipenv_shell(self, runner, cli):
    #     with runner.isolated_filesystem():
    #         fake_dir = 'fake_dir'
    #         os.mkdir(fake_dir)
    #         os.chdir(fake_dir)
    #         proc = call_pipenv_shell(project_dir=fake_dir, envname='CustomPrompt')
    #         proc
    #         import pdb; pdb.set_trace()

    def test_find_environments(self, runner, cli):
        find_environments


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
