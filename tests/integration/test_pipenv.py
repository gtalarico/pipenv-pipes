import pytest  # noqa: F401
from pexpect.popen_spawn import PopenSpawn
import subprocess

from pipenv_pipes.pipenv import (
    call_pipenv_venv,
    call_pipenv_shell,
)


def test_call_pipenv_venv_not_a_venv(temp_empty):
    """ call venv on orphan folder: No virtual path has been created """
    output, code = call_pipenv_venv(temp_empty)
    assert code != 0
    assert 'no virtualenv has been create' in output.lower()


@pytest.mark.skip(reason='Need mock pipenv')
def test_call_pipenv_venv(project_dir):
    pass  # Test when it works, needs mock pipenv


# Test Shell as Integration Only
@pytest.mark.skip(reason='Need mock pipenv')
def test_call_pipenv_shell(runner, temp_empty):
    output, code, proc = call_pipenv_shell(cwd=temp_empty)
    # assert code == 0
    # assert output == 'x'
    # proc = PopenSpawn('pipes proj', cwd=temp_empty)
    # proc.sendline('exit')
    # output = proc.
