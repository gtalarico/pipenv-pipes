import os
import sys
from subprocess import Popen, PIPE


def PipedPopen(cmds, **kwargs):
    """ Helper Piped Process for drier code"""
    timeout = kwargs.pop('timeout', None)
    env = kwargs.pop('env', dict(os.environ))
    proc = Popen(
        cmds,
        stdout=PIPE,
        stderr=PIPE,
        env=env,
        **kwargs
    )
    out, err = proc.communicate(timeout=timeout)
    output = out.decode().strip() or err.decode().strip()
    code = proc.returncode
    return output.strip(), code


def call_pipenv_venv(project_dir, timeout=10):
    """ Calls ``pipenv --venv`` from a given project directory """
    output, code = PipedPopen(cmds=['pipenv', '--venv'], cwd=project_dir)
    return output, code


def call_pipenv_shell(cwd, envname='pipenv-shell', timeout=None):
    """ Calls ``pipenv shell``` from a given envname """
    environ = dict(os.environ)
    environ['PROMPT'] = '({}){}'.format(envname, os.getenv('PROMPT', ''))

    is_test = 'PYTEST_CURRENT_TEST' in os.environ
    stdout = PIPE if is_test else sys.stdout
    stderr = PIPE if is_test else sys.stderr

    proc = Popen(
        ['pipenv', 'shell'],
        cwd=cwd,
        shell=False,
        stdout=stdout,
        stderr=stderr,
        env=environ,
        )
    out, err = proc.communicate(timeout=timeout)
    output = out or err
    code = proc.returncode
    return output, code, proc


def call_python_version(pybinpath):
    binpath = os.path.dirname(pybinpath)
    pybinpath = os.path.join(binpath, 'python')
    output, code = PipedPopen(cmds=[pybinpath, '--version'])
    return output, code
