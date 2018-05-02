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
    set_project_dir,
    get_envname_index,
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


# @click.group(invoke_without_command=True)
@click.command()
@click.argument('envname', required=False)
@click.option('--list', '-l', 'list_', is_flag=True, help='List Pipenv Projects')
@click.option('--set', '-s', 'set_', is_flag=True, help='Set Project Directory for the Enviroment')
@click.option('--setdir', '-d', 'setdir', help='Project Directory',
              default='.', type=click.Path(exists=True, resolve_path=True))
@click.option('--verbose', '-v', is_flag=True, help='Verbose')
@click.pass_context
def pipes(ctx, envname, list_, set_, setdir, verbose):
    """ Pipenv Environment Switcher """

    if not envname or list_:
        _print_project_list(projects=PROJECTS, verbose=verbose)
        err = "\nUse pipes --help for usage"
        click.echo(err, err=True)
        ctx.exit()

    # Check if using index and if yes launch
    project_index = get_envname_index(envname)
    if project_index:
        project = PROJECTS[project_index]

    # Envname check
    matches = get_matches(PROJECTS, envname)
    project = ensure_one_match(envname, matches)

    if not set_:
        launch_env(project)
    else:
        set_env_dir(
            envname=project.envname,
            envpath=project.envpath,
            setdir=setdir)


def set_env_dir(envname, envpath, setdir):
    click.echo("Setting Environment '{}'".format(envname))
    click.echo("To Project Directory '{}'".format(setdir))

    if click.confirm('Confirm?', default=True):
        set_project_dir(envpath, setdir)

        msg = ("Project Direectory Set.\n"
               "To modify the directory edit the '.project' in the enviroment"
               "or run the 'pipes --set' command again")

        click.echo(msg)

    sys.exit(0)


def launch_env(project):
    """ Launch Pipenv Shell """

    project_dir = ensure_has_project_dir_file(project)
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

    sys.exit(0)


def _print_project_list(projects, verbose):
    """ Prints Enviroments List """
    header = '[ Pipenv Enviroments ] '
    if verbose:
        header += ' {}'.format(PIPENV_HOME)
    click.echo(click.style(header, fg='white', bold=True))

    for index, project in enumerate(projects):
        project_dir = get_project_dir(project)
        has_project_dir = bool(project_dir)
        name = click.style(project.envname, fg='yellow')
        path = click.style(project.envpath, fg='blue')
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

def ensure_has_project_dir_file(project):
    """
    Ensures the enviromend has .project file.
    If check failes, error is printed recommending course of action
    """
    project_dir = get_project_dir(project)

    if project_dir:
        return project_dir

    else:
        msg = ("Pipenv enviroment '{env}' does not have set a project path.\n"
               "Use 'pipes set' to set the directory for this enviroment\n\n"
               "$ pipes set {env} [projectpath]".format(env=project.envname))
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
        return matches[0]


if __name__ == "__main__":
    sys.exit(entry())
