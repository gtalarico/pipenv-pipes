===================================
Pipes
===================================

Friendly Pipenv Environment Switcher for your shell


.. image:: https://img.shields.io/pypi/v/pipenv_pipes.svg
        :target: https://pypi.python.org/pypi/pipenv_pipes
        :alt: Pypi Badge

.. image:: https://img.shields.io/travis/gtalarico/pipenv_pipes.svg
        :target: https://travis-ci.org/gtalarico/pipenv_pipes
        :alt: Traves CI Badge

.. image:: https://img.shields.io/codecov/c/github/gtalarico/pipenv-pipes.svg
        :target: https://codecov.io/gh/gtalarico/pipenv-pipes
        :alt: Codecov Badge

.. image:: https://readthedocs.org/projects/pipenv-pipes/badge/?version=latest
        :target: https://pipenv-pipes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Overview
---------

Pipes is a Pipenv-companion CLI tool that provides a quick way to jump between your pipenv powered projects.


* Documentation: https://pipenv-pipes.readthedocs.io.

.. image:: https://raw.githubusercontent.com/gtalarico/pipenv-pipes/master/docs/static/pipes-gif.gif


Install
--------

.. code:: python

    >>> pip install pipenv-pipes

Usage
--------

List available Pipenv Environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

  >>> pipes

.. code:: bash

  [ Pipenv Environments ]
    0: project1-LwEMcb8W *
    1: project2-R1v7_ynT *


\* Indicates the Environment already has a Project Directory associated.


Activate Pipenv Enviroment Shell
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

    $ pipes project1

This would cd into directory '`/path/to/project1'` and the corresponding Pipenv Shell is activated.

If query term (``project1``) returns 2 or more matches, a more specific query term needs to be used.
For instance, to match ``0: project1-LwEMcb8W`` user would need to type ``project1`` or ``Lw` to get a single match.
If ``envname`` argument was ``project``, activation would fail since Pipes cannot guess which enviroment users wants (```project1`` or ``project2``).

The environment index can also be used. To active the enviroment ``1: project2-R1v7_ynT`` user would run:

.. code:: bash

    $ pipes 1:


Link Pipenv Environment to a Project Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you can switch into a project using Pipes, the selected environment must have a project directory associated with it.

To link a project directory with its environment run:

.. code:: bash

    $ pipes --link /path/to/project1

Pipes will find the associated Pipenv Environmnet by using ``pipenv --venv`` from that location,
and then store the project directory path within the environment (``.project`` file)

This pattern is similar to what virtualenvwrapper's ``workon`` uses to link a VirtualEnviroment folder to
the corresponding project.

Environments that have associated project folders are shown with an asterisk `*` on the Pipenv Environment list:

.. code:: bash

    $ pipes --list

To see a detail output of the enviroments and the corresponding paths use the ``--verbose`` option:

.. code:: bash

    $ pipes -0-verbose

.. code:: bash

    [ Pipenv Environments ]  /Users/gtalarico/.local/share/virtualenvs
      0: project1-LwEMcb8W
         Environment: /Users/gtalarico/.local/share/virtualenvs/flask-vue-LwEMcb8W
         Project Dir: /Users/gtalarico/dev/flask-vue
      1: project2-R1v7_ynT
         Environment: /Users/gtalarico/.local/share/virtualenvs/genome-R1v7_ynT
         Project Dir: /Users/gtalarico/dev/genome



Other Commands
^^^^^^^^^^^^^^

For more details check ``pipes --help``


Todo
-------

* Add Documentation
* Add tests + Contributing
* Setup Travis CI
* Add cd-only flag (don't activate shell)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
