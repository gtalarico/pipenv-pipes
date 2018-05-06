import pytest  # noqa: F401

from pipenv_pipes.cli import pipes
from pipenv_pipes.pipenv import (
    call_pipenv_venv,
    call_pipenv_shell,
)


def test_cli_run(runner):
    """Test the CLI."""
    result = runner.invoke(pipes)
    assert result.exit_code == 0

def test_call_pipenv_venv_not_a_venv(temp_empty):
    """ call venv on orphan folder: No virtual path has been created """
    path, error = call_pipenv_venv(temp_empty)
    assert not path
    assert error

@pytest.mark.skip(reason='Need better popen control')
def test_call_pipenv_shell(temp_empty):
    proc, out, err = call_pipenv_shell(
        cwd=temp_empty,
        timeout=15,
        pipe=True)
    # This passes with pytest -s
    # but fails without since pytest interferes with the stdout/stferr
    # Capturing
    # assert proc.returncode == -9
    assert "Use 'exit' to leave" in err
