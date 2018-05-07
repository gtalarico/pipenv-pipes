import pytest  # noqa: F401
import os

from pipenv_pipes.pipenv import (
    call_pipenv_venv,
    call_pipenv_shell,
)


def test_call_pipenv_venv_not_a_venv(temp_folder):
    """ call venv on orphan folder: No virtual path has been created """
    output, code = call_pipenv_venv(temp_folder)
    assert code != 0
    assert 'no virtualenv has been create' in output.lower()


@pytest.mark.slow
def test_call_pipenv_venv(mock_env_home_slow):
    pipenv_home, mock_projects_dir = mock_env_home_slow
    for project_name in os.listdir(mock_projects_dir):
        project_dir = os.path.join(mock_projects_dir, project_name)
        output, code = call_pipenv_venv(project_dir=project_dir)
        assert code == 0
        assert pipenv_home in output


@pytest.mark.skip(reason='Not Sure how to mock this. Tested in test_cli')
def test_call_pipenv_shell(temp_folder):
    output, code, proc = call_pipenv_shell(cwd=temp_folder)
