===================================
Pipes
===================================


A friendly Pipenv Environment Switcher for your shell


.. image:: https://img.shields.io/pypi/v/pipenv_pipes.svg
        :target: https://pypi.python.org/pypi/pipenv_pipes
        :alt: Pypi Badge

.. image:: https://img.shields.io/travis/gtalarico/pipenv-pipes/master.svg
        :target: https://travis-ci.org/gtalarico/pipenv-pipes
        :alt: Traves CI Badge

.. image:: https://img.shields.io/codecov/c/github/gtalarico/pipenv-pipes.svg
        :target: https://codecov.io/gh/gtalarico/pipenv-pipes
        :alt: Codecov Badge

.. image:: https://readthedocs.org/projects/pipenv-pipes/badge/?version=latest
        :target: https://pipenv-pipes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Overview
---------

Pipes is a Pipenv companion CLI tool that provides a quick way to jump between your pipenv powered projects.


* Documentation: https://pipenv-pipes.readthedocs.io.

.. image:: https://raw.githubusercontent.com/gtalarico/pipenv-pipes/master/docs/static/pipes-gif.gif

Install
--------

.. code:: bash

    $ pip install pipenv-pipes


Usage
--------

List available Pipenv Environments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

  $ pipes
  or
  $ pipes --list

.. code:: bash

  [ Pipenv Environments ]
    0: project1-LwEMcb8W *
    1: project2-R1v7_ynT *


\* Indicates the Environment already has a Project Directory associated.


To see a detail output of the enviroments and the corresponding paths use the ``--verbose`` option:

.. code:: bash

    $ pipes --list -verbose

.. code:: bash

    [ Pipenv Environments ]  /Users/gtalarico/.local/share/virtualenvs
    
      0: project1-LwEMcb8W
         Environment: /Users/gtalarico/.local/share/virtualenvs/project1-LwEMcb8W
         Project Dir: /Users/gtalarico/dev/flask-vue
         
      1: project2-R1v7_ynT
         Environment: /Users/gtalarico/.local/share/virtualenvs/project2-R1v7_ynT
         Project Dir: /Users/gtalarico/dev/genome
         
*Project Dir* for unlinked Environments will show as `Not Set`.


To understand how Pipes links a Procject Directory with its corresponding VirtualEnv see `Link Pipenv Environment to a Project Directory`_.


Link Pipenv Environment to a Project Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you can switch into a project using Pipes, the selected environment must have a project directory associated with it.

To link a project directory with its environment run:

.. code:: bash

    $ pipes --link /path/to/project1

Pipes will find the associated Pipenv Environmnet by running ``pipenv --venv`` from from the target directory.
Once detected, the project directory path is stored within the environment inside a ``.project`` file.

This pattern is the same used by virtualenvwrapper.


Go To a Project by Name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you the Virtual Enviromnents are asscociated with Project Directories we can use the commands below to navigate our projects.

To go to a project run `pipes` followed by the name of a project:

.. code:: bash

    $ pipes project1

This would cd into directory ``/path/to/project1`` and the corresponding Pipenv Shell is activated.

If query term (eg. ``project1``) returns two or more matches, a more specific query term needs to be used.

For instance, to match ``0: project1-LwEMcb8W`` user would need to type ``project1`` to get a single match.

If query argument was ``project`` activation would fail since Pipes cannot guess which enviroment users wants 
(```project1`` or ``project2``).


Go To a Project by Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The environment index can also be used. 
To active the enviroment ``1: project2-R1v7_ynT``:

.. code:: bash

    $ pipes 1:



Unlink a Project
^^^^^^^^^^^^^^^^^

To unlink a project1 directory from its Pipenv Enviroment run:

.. code:: bash

    $ pipes --unlink project1


Other Commands
^^^^^^^^^^^^^^

For more details check ``pipes --help``


Credits
-------

Send me a message on twitter_

.. _twitter: https://twitter.com/gtalarico


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
