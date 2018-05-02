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
    get_projects,
    get_matches,
    get_project_dir,
    set_project_dir
)

# CLI Constants
PROJECTS = get_projects(PIPENV_HOME)
NUM_PROJECTS = len(PROJECTS)


def entry():
    """ Pipes Entry Point """

    if PIPENV_ACTIVE:
        msg = ("Pipenv Shell is already active. \n"
               "Use 'exit' to close the shell before starting a new one.")
        click.echo(click.style(msg, fg='red'))
        return

    if VENV_IS_ACTIVE:
        msg = ("A Virtual Environemnt is already active.\n"
               "Use 'deactivate' to close disable the enviroment "
               "before starting a new one.")
        click.echo(click.style(msg, fg='red'))
        return

    if PIPENV_VENV_IN_PROJECT:
        msg = 'PIPENV_VENV_IN_PROJECT is not supported at this time'
        click.echo(click.style(msg, fg='red'))
        return

    if not PROJECTS:
        click.echo('No pipenv projects found in {}'.format(PIPENV_HOME))
        return

    pipes()


@click.group(invoke_without_command=True)
@click.pass_context
def pipes(ctx):
    """ pipes Project Switcher """
    if not ctx.invoked_subcommand:
        ctx.invoke(list_envs)
        err = "\nUse pipes --help for usage"
        click.echo(err, err=True)


@pipes.command(name='list')
@click.option('--verbose', '-v', is_flag=True, help='Verbose')
def list_envs(verbose):
    """ List Pipenv Projects """
    _print_project_list(projects=PROJECTS, verbose=verbose)


@pipes.command(name='go')
@click.option(
    '--index', '-i',
    required=False,
    help='Index of Project in list',
    type=click.IntRange(0, NUM_PROJECTS - 1))
@click.argument(
    'query',
    metavar='[EnvName]',
    required=False,
    type=click.STRING,
    default='')
@click.pass_context
@click.option('--verbose', '-v', is_flag=True, help='Verbose')
def go(ctx, index, query, verbose):
    """ Activate Pipenv Shell """

    # Check if it has index or query
    if not index and not query:
        # ctx.invoke(list_envs)
        raise click.UsageError('EnvName or index are required')

    # Both Options, not allowed
    if index and query:
        err_msg = click.style(
            "index option cannot be used with project name", fg='red')
        click.echo(err_msg)
        return

    # Has index Retrieved project
    if index:
        project = PROJECTS[index]
        _launch_env(project)
    matches = get_matches(PROJECTS, query)
    _validate_one_match(query, matches)
    project = matches[0]
    _launch_env(project)


@pipes.command()
@click.argument('query', metavar='envname')
@click.argument('project_dir', type=click.Path(exists=True, resolve_path=True))
def set(query, project_dir):
    matches = get_matches(PROJECTS, query)
    _validate_one_match(query, matches)
    project = matches[0]
    set_project_dir(project.envpath, project_dir)

    click.echo(
        "Enviroment: '{}' \nSet to directory '{}'".format(project.envpath,
                                                            project_dir))


def _launch_env(project):
    """ Launch Pipenv Shell """
    try:
        project_dir = get_project_dir(project)
    except IOError:
        msg = ("Pipenv enviroment '{env}' does not have set a project path.\n"
               "Use 'pipes set' to set the directory for this enviroment\n\n"
               "$ pipes set {env} [projectpath]".format(env=project.envname))
        click.echo(click.style(msg, fg='red'), err=True)
        sys.exit()

    click.echo("Project dir is '{}'".format(project_dir))
    click.echo("Environment is '{}'".format(project.envpath))

    if click.confirm('Activate?', default=True):
        env = os.environ.copy()
        env['PROMPT'] = '({}){}'.format(project.envname, PROMPT)
        os.chdir(project_dir)
        out = subprocess.call(
            'cd {dir} & pipenv shell'.format(dir=project_dir),
            shell=True, env=env)
        click.echo('Terminating pipes Shell...')
    sys.exit()


def _print_project_list(projects, verbose):
    """ Prints Projects List """
    header = '[ Pipenv Projects ] '
    if verbose:
        header += ' {}'.format(PIPENV_HOME)
    click.echo(click.style(header, fg='white', bold=True))

    for index, project in enumerate(projects):
        name = click.style(project.envname, fg='yellow')
        path = click.style(project.envpath, fg='white')
        index = click.style(str(index), fg='red')
        numbered = ' {} : {}'.format(index, name)
        if not verbose:
            click.echo(numbered)
        else:
            click.echo('{} {}'.format(numbered, path))


def _validate_one_match(query, matches):
    """
    Checks Matches and prints messages if validation does not pass
    Returns True if passes validation
    """

    # No Matches
    if not matches:
        err_msg = click.style(
            "No projec matches for query '{}'\n".format(query), fg='red')
        click.echo(err_msg)
        _print_project_list(PROJECTS, verbose=False)
        sys.exit(1)

    # 2+ Matches
    elif len(matches) > 1:
        msg = ("Query '{}' matches more than one project (shown below)."
               "Try using a more sepecific query term.\n".format(query))
        click.echo(click.style(msg, fg='red'), err=True)
        _print_project_list(matches, verbose=False)
        sys.exit(1)

    else:
        return True


if __name__ == "__main__":
    sys.exit(entry())
