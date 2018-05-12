import pytest  # noqa: F401
import os

from pipenv_pipes.pipenv import (
    call_pipenv_venv,
    # call_python_version
    # call_pipenv_shell,
)


def test_call_pipenv_venv_not_a_venv(temp_folder):
    """ call venv on orphan folder: No virtual path has been created """
    output, code = call_pipenv_venv(temp_folder)
    assert code != 0
    assert 'no virtualenv has been created' in output.lower()


def test_call_pipenv_venv(mock_env_home):
    pipenv_home, mock_projects_dir = mock_env_home
    first_project = os.listdir(mock_projects_dir)[0]
    project_dir = os.path.join(mock_projects_dir, first_project)
    output, code = call_pipenv_venv(project_dir=project_dir)
    assert first_project in output
    assert code == 0
    assert pipenv_home in output


@pytest.mark.skip
def test_call_python_version(mock_env_home, project_names):
    """ Tested in test_core + cli  """

@pytest.mark.skip
def test_call_pipenv_shell(mock_env_home):
    """ This does not guarantee the shell was launched successful,
    however it ensure it timed out, which means the command did went through
    and it was open for at least 5 seconds which means the shell was most
    likely opened """
    # pipenv_home, mock_projects_dir = mock_env_home
    # project_name = os.listdir(mock_projects_dir)[0]
    # project_dir = os.path.join(mock_projects_dir, project_name)
    # import pdb; pdb.set_trace()
    # with pytest.raises(TimeoutExpired):
    # import pdb; pdb.set_trace()
    # output = call_pipenv_shell(cwd=project_dir, timeout=5)
