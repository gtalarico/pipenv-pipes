import os
import subprocess


def call_pipenv(*args, pipe=False, timeout=30, **kwargs):
    if pipe:
        kwargs.update(dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ))
    proc = subprocess.Popen(
        ['pipenv'] + list(args),   # *args fails on <= 3.4
        universal_newlines=True,  # Returns String instead of bytes
        **kwargs)
    try:
        output, err = proc.communicate(timeout=timeout)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        proc.kill()
        output, err = proc.communicate()
    else:
        pass
    finally:
        return proc, output, err


def call_pipenv_venv(project_dir, timeout=10):
    """ Calls ``pipenv --venv`` from a given project directory """
    proc, output, err = call_pipenv(
        '--venv',
        pipe=True,
        cwd=project_dir,
        timeout=timeout
    )
    return output.strip(), err.strip()


def call_pipenv_shell(cwd, envname='pipenv-shell', timeout=None, pipe=False):
    """ Calls ``pipenv shell``` from a given envname """
    environ = dict(os.environ)
    environ['PROMPT'] = '({}){}'.format(envname, os.getenv('PROMPT', ''))
    proc, output, err = call_pipenv(
        'shell',
        cwd=cwd,
        timeout=timeout,
        pipe=pipe,  # True For test only
        )
    return proc, output, err
