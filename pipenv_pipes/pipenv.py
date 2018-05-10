import os
import sys
from subprocess import Popen, PIPE


def PipedPopen(*args, **kwargs):
    """ Helper Piped Process for drier code"""
    timeout = kwargs.pop('timeout', None)
    proc = Popen(*args, **kwargs,
                 stdout=PIPE,
                 stderr=PIPE,
                 universal_newlines=True,
                )
    out, err = proc.communicate(timeout=timeout)
    output = out.strip() or err.strip()
    code = proc.returncode
    return output.strip(), code


def call_pipenv_venv(project_dir, timeout=10):
    """ Calls ``pipenv --venv`` from a given project directory """
    output, code = PipedPopen(['pipenv', '--venv'], cwd=project_dir)
    return output, code


def call_pipenv_shell(cwd, envname='pipenv-shell'):
    """ Calls ``pipenv shell``` from a given envname """
    environ = dict(os.environ)
    environ['PROMPT'] = '({}){}'.format(envname, os.getenv('PROMPT', ''))

    is_test = 'PYTEST_CURRENT_TEST' in os.environ
    timeout = 10 if is_test else None
    stdout = PIPE if is_test else sys.stdout

    proc = Popen(
        ['pipenv', 'shell'],
        cwd=cwd,
        shell=False,
        stdout=stdout,
        )

    out, err = proc.communicate(timeout=timeout)
    output = out or err
    code = proc.returncode
    return output, code, proc
