# -*- coding: utf-8 -*-

""" Pipes: Pipenv Shell Switcher """

import os
import sys
import click

from . import __version__
from .environment import EnvVars
from .utils import get_query_matches, get_index_from_query
from .pipenv import (
    call_pipenv_venv,
    call_pipenv_shell,
)
from .core import (
    find_environments,
    read_project_dir_file,
    delete_project_dir_file,
    write_project_dir_project_file,
)


@click.command()
@click.argument('envname', required=False)
@click.option(
    '--list', 'list_',
    is_flag=True,
    help='List Pipenv Projects')
@click.option(
    '--link', '-l', 'setlink',
    help='Crete Environment Link to the Target Project Directory',
    metavar='<ProjectDir>',
    required=False,
    type=click.Path(exists=True, resolve_path=True)
    )
@click.option('--unlink', '-u', 'unlink',
              is_flag=True,
              help='Unlink Project Directory from this Environment')
@click.option('--verbose', '-v', is_flag=True, help='Verbose')
@click.option('--version', is_flag=True, help='Show Version')
@click.pass_context
def pipes(ctx, envname, list_, setlink, unlink, verbose, version):
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
    if version:
        click.echo(__version__)
        return

    env_vars = EnvVars()
    ensure_env_vars_are_ok(env_vars)
    environments = find_environments(env_vars.PIPENV_HOME)
    if not environments:
        click.echo(
            'No pipenv environments found in {}'.format(env_vars.PIPENV_HOME))
        sys.exit(1)

    if list_ or (not envname and not setlink):
        if verbose:
            click.echo('PIPENV_HOME: {}'.format(env_vars.PIPENV_HOME))

        print_project_list(environments=environments, verbose=verbose)
        msg = "\nCheck 'pipes --help' for usage"
        click.echo(msg)
        sys.exit(0)

    if setlink and envname:
        msg = ("--link cannot be user with envname query")
        raise click.UsageError(msg)

    if setlink:
        set_env_dir(project_dir=setlink)

    # Check if using index and if yes launch
    env_index = get_index_from_query(query=envname)
    if env_index:
        ensure_valid_index(env_index=env_index, environments=environments)
        environment = environments[env_index]

    else:
        # Envname check
        matches = get_query_matches(environments, envname)
        environment = ensure_one_match(envname, matches, environments)

    if unlink:
        if delete_project_dir_file(environment.envpath):
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

    click.echo("Found Environment: ", nl=False)
    click.echo(click.style(project_dir_envpath, fg='blue'))

    write_project_dir_project_file(project_dir_envpath, project_dir)
    msg = ("\nProject Directory Set.")
    click.echo(click.style(msg, fg='yellow'))

    sys.exit(0)


def launch_env(environment):
    """ Launch Pipenv Shell """

    project_dir = ensure_has_project_dir_file(environment)
    click.echo("Project dir is '{}'".format(project_dir))
    click.echo("Environment is '{}'".format(environment.envpath))

    ensure_project_dir_has_env(project_dir)
    call_pipenv_shell(cwd=project_dir, envname=environment.envname)
    msg = 'Terminating Pipes Shell...'
    click.echo(click.style(msg, fg='red'))
    sys.exit(0)


def print_project_list(environments, verbose):
    """ Prints Environments List """
    # import os; os.system('clear')
    header = '[ Pipenv Environments ] '
    click.echo(click.style(header, bold=True))

    for index, environment in enumerate(environments):
        project_dir = read_project_dir_file(environment.envpath)
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
    project_dir = read_project_dir_file(environment.envpath)

    if project_dir:
        return project_dir

    else:
        msg = (
            "Pipenv enviroment '{env}' does not have project directory.\n"
            "Use 'pipes --link <project-dir>' to link a project directory\n"
            "with this enviroment".format(env=environment.envname))

        click.echo(click.style(msg, fg='red'), err=True)
        sys.exit(0)


def ensure_one_match(query, matches, environments):
    """
    Checks envname query matches exactly one match.
    If matches zero, project list is printed.
    If matches >= 2, matching project list is printed.
    In both cases, program exists if validation fails.
    """

    # No Matches
    if not matches:
        err_msg = click.style(
            "No matches for query '{}'\n".format(query), fg='red')
        click.echo(err_msg)
        print_project_list(environments=environments, verbose=False)
        sys.exit(0)

    # 2+ Matches
    elif len(matches) > 1:
        msg = ("Query '{}' matches more than one environment (shown below)."
               "Try using a more sepecific query term.\n".format(query))
        click.echo(click.style(msg, fg='red'), err=True)
        print_project_list(environments=matches, verbose=False)
        sys.exit(0)

    else:
        return matches[0]


def ensure_project_dir_has_env(project_dir):
    output, code = call_pipenv_venv(project_dir)
    if code == 0:
        envpath = output
        return envpath
    else:
        click.echo(click.style(output, fg='red'), err=True)
        sys.exit(1)


def ensure_valid_index(env_index, environments):
    if env_index not in range(0, len(environments)):
        raise click.UsageError('Invalid Environment Index')


def ensure_env_vars_are_ok(env_vars):
    error_msg = env_vars.validate_environment()
    if error_msg:
        click.echo(click.style(error_msg, fg='red'))
        sys.exit(1)
