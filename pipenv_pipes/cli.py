# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import sys
import click
import subprocess

from .environment import (
    PIPENV_HOME,
    PIPENV_ACTIVE,
    PROMPT,
    PIPENV_VENV_IN_PROJECT,
    VENV_IS_ACTIVE,
)

from .utils import (
    get_environments,
    get_matches,
    get_project_dir,
    get_envname_index,
    get_env_path_from_project_dir,
    unset_project_dir,
    set_project_dir_project_file,
)

if not os.path.exists(PIPENV_HOME):
    msg = ('Could not find Pipenv Environments location. [{}] \n'
            'If you are using a non-default location you will need to '
            'add the path to $WORKON_HOME.'.format(PIPENV_HOME))
    click.echo(click.style(msg, fg='red'))
    sys.exit(1)

if PIPENV_ACTIVE:
    msg = ("Pipenv Shell is already active. \n"
            "Use 'exit' to close the shell before starting a new one.")
    click.echo(click.style(msg, fg='red'))
    sys.exit(1)

if VENV_IS_ACTIVE:
    msg = ("A Virtual Environemnt is already active.\n"
            "Use 'deactivate' to close disable the enviroment "
            "before starting a new one.")
    click.echo(click.style(msg, fg='red'))
    sys.exit(1)

if PIPENV_VENV_IN_PROJECT:
    msg = 'PIPENV_VENV_IN_PROJECT is not supported at this time'
    click.echo(click.style(msg, fg='red'))
    sys.exit(1)

# Set Environments
ENVIRONMENTS = get_environments(PIPENV_HOME)
NUM_ENVIRONMENTS = len(ENVIRONMENTS)
if not ENVIRONMENTS:
    click.echo('No pipenv environments found in {}'.format(PIPENV_HOME))
    sys.exit(1)


def entry():
    """ Pipes Entry Point """
    pipes()


@click.command()
@click.argument('envname', required=False)
@click.option('--list', '-l', 'list_', is_flag=True,
              help='List Pipenv Projects')
@click.option('--link', '-l', 'setlink',
              help='Crete Environment Link to the Target Project Directory',
              metavar='<ProjectDir>',
              required=False, type=click.Path(exists=True, resolve_path=True))
@click.option('--unlink', '-u', 'unlink',
              is_flag=True,
              help='Unlink Project Directory from this Environment')
@click.option('--verbose', '-v', is_flag=True, help='Verbose')
@click.pass_context
def pipes(ctx, envname, list_, setlink, unlink, verbose):
    """

    Pipes - PipEnv Environment Switcher

    Go To Project:\n
        >>> pipes envname

    Set Project Directory:\n
        >>> pipes --link path/to/project/path

    Unset Project Directory:\n
        >>> pipes envname --unlink

    Remove link between enviroment and project directory

    See all Pipenv Environments:\n
        >>> pipes --list
        >>> pipes --list --verbose

    """

    if list_ or (not envname and not setlink):
        print_project_list(environments=ENVIRONMENTS, verbose=verbose)
        err = "\nCheck 'pipes --help' for usage"
        click.echo(err, err=True)
        sys.exit(0)

    if setlink and envname:
        msg = ("--link cannot be user with envname query")
        raise click.UsageError(msg)

    if setlink:
        set_env_dir(project_dir=setlink)

    # Check if using index and if yes launch
    project_index = get_envname_index(envname)
    if project_index:
        environment = ENVIRONMENTS[project_index]

    else:
        # Envname check
        matches = get_matches(ENVIRONMENTS, envname)
        environment = ensure_one_match(envname, matches)

    if unlink:
        if unset_project_dir(environment.envpath):
            click.echo(
                'Project directory cleared [{}]'.format(environment.envpath))
        else:
            click.echo('Project directory was already clear.')
        sys.exit(0)

    else:
        launch_env(environment)


# def set_env_dir(envname, envpath, project_dir):
def set_env_dir(project_dir):

    click.echo('Target Project Directory is: ', nl=False)
    click.echo(click.style(project_dir, fg='blue'))
    click.echo('Looking for associated Pipenv Environment...')

    # Before setting project_dir, let's make sure directory is actually
    # Associated with the env, otherwise activation will not work
    project_dir_envpath = ensure_project_dir_has_env(project_dir)

    click.echo("Environment is: ", nl=False)
    click.echo(click.style(project_dir_envpath, fg='blue'))

    prompt = click.style(
        'Set Project Directory + Environment association?', fg='yellow')

    if click.confirm(prompt):
        set_project_dir_project_file(project_dir_envpath, project_dir)
        msg = ("\nProject Direectory Set.")

        click.echo(click.style(msg, bold=True))

    sys.exit(0)


def launch_env(environment):
    """ Launch Pipenv Shell """

    project_dir = ensure_has_project_dir_file(environment)
    click.echo("Project dir is '{}'".format(project_dir))
    click.echo("Environment is '{}'".format(environment.envpath))


    ensure_project_dir_has_env(project_dir)

    env = os.environ.copy()
    env['PROMPT'] = '({}){}'.format(environment.envname, PROMPT)
    os.chdir(project_dir)
    out = subprocess.call(
        'cd {dir} & pipenv shell'.format(dir=project_dir),
        shell=True, env=env)
    click.echo('Terminating pipes Shell...')

    sys.exit(0)


def print_project_list(environments, verbose):
    """ Prints Environments List """
    header = '[ Pipenv Environments ] '
    if verbose:
        header += ' {}'.format(PIPENV_HOME)
    click.echo(click.style(header, bold=True))

    for index, environment in enumerate(environments):
        project_dir = get_project_dir(environment)
        has_project_dir = bool(project_dir)
        name = click.style(environment.envname, fg='yellow')
        path = click.style(environment.envpath, fg='blue')
        index = click.style(str(index), fg='red')

        entry = ' {}: {}'.format(index, name)

        if not verbose:
            entry = entry if not has_project_dir else entry + ' *'
            click.echo(entry)
        else:
            empty = click.style('NOT SET', fg='red')
            project_dir = project_dir if has_project_dir else empty
            click.echo(
                '{} \n    Environment: {}\n    Project Dir: {}'.format(
                    entry,
                    path,
                    project_dir))

def ensure_has_project_dir_file(environment):
    """
    Ensures the enviromend has .project file.
    If check failes, error is printed recommending course of action
    """
    project_dir = get_project_dir(environment)

    if project_dir:
        return project_dir

    else:
        msg = (
            "Pipenv enviroment '{env}' does not have project directory.\n"
            "Use 'pipes --link <project-dir>' to link a project directory"
            "with this enviroment".format(env=environment.envname))

        click.echo(click.style(msg, fg='red'), err=True)
        sys.exit()

def ensure_one_match(query, matches):
    """
    Checks envname query matches exactly one match.
    If matches zero, project list is printed.
    If matches >= 2, matching project list is printed.
    In both cases, program exists if validation fails.
    """

    # No Matches
    if not matches:
        err_msg = click.style(
            "No projec matches for query '{}'\n".format(query), fg='red')
        click.echo(err_msg)
        print_project_list(environments=ENVIRONMENTS, verbose=False)
        sys.exit(1)

    # 2+ Matches
    elif len(matches) > 1:
        msg = ("Query '{}' matches more than one project (shown below)."
               "Try using a more sepecific query term.\n".format(query))
        click.echo(click.style(msg, fg='red'), err=True)
        print_project_list(environments=matches, verbose=False)
        sys.exit(1)

    else:
        return matches[0]


def ensure_project_dir_has_env(project_dir):
    envpath = get_env_path_from_project_dir(project_dir)
    if envpath:
        return envpath
    else:
        msg = (
            "\nThe target Project Directocd ry is not "
            "associated with any Pipenv Environments.")
        click.echo(click.style(msg, fg='red'))
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(entry())
