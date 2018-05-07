import os
import sys

import subprocess
from pexpect.popen_spawn import PopenSpawn


def call_pipenv(*args, pipe=False, timeout=30, **kwargs):
    pass
    # proc = subprocess.Popen(
    #     ['pipenv'] + list(args),   # *args fails on <= 3.4
    #     universal_newlines=True,  # Returns String instead of bytes
    #     **kwargs)
    # try:
    #     output, err = proc.communicate(timeout=timeout)
    # except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
    #     proc.kill()
    #     output, err = proc.communicate()
    # else:
    #     pass
    # finally:
    #     return proc, output, err


def call_pipenv_venv(project_dir, timeout=10):
    """ Calls ``pipenv --venv`` from a given project directory """
    proc = PopenSpawn(
        'pipenv --venv',
        cwd=project_dir,
        timeout=timeout)
    code = proc.wait()
    output = proc.readline().decode().strip()
    return output, code


def call_pipenv_shell(cwd, envname='pipenv-shell'):
    """ Calls ``pipenv shell``` from a given envname """
    environ = dict(os.environ)
    environ['PROMPT'] = '({}){}'.format(envname, os.getenv('PROMPT', ''))

    is_test = 'PYTEST_CURRENT_TEST' in os.environ
    timeout = 5 if is_test else None
    stdout = subprocess.PIPE if is_test else sys.stdout

    proc = subprocess.Popen(
        ['pipenv', 'shell'],
        cwd=cwd,
        shell=False,
        stdout=stdout,
        )

    out, err = proc.communicate(timeout=timeout)
    output = out or err
    code = proc.returncode
    return output, code, proc
