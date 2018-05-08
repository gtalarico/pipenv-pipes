===================================
Pipes
===================================


Pipenv Environment Switcher ⚡


.. image:: https://img.shields.io/pypi/v/pipenv_pipes.svg
        :target: https://pypi.python.org/pypi/pipenv_pipes
        :alt: Pypi

.. image:: https://travis-ci.org/gtalarico/pipenv-pipes.svg?branch=master
        :target: https://travis-ci.org/gtalarico/pipenv-pipes
        :alt: Traves CI

.. image:: https://codecov.io/gh/gtalarico/pipenv-pipes/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/gtalarico/pipenv-pipes
        :alt: Codecov

.. image:: https://readthedocs.org/projects/pipenv-pipes/badge/?version=latest
        :target: https://pipenv-pipes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation


Overview
---------

Pipes is a Pipenv companion CLI tool that provides a quick way to jump between your pipenv powered projects.

.. image:: https://raw.githubusercontent.com/gtalarico/pipenv-pipes/master/docs/static/pipes-gif.gif

Documentation
-------------

https://pipenv-pipes.readthedocs.io


Install
--------

.. code:: bash

    $ pip install pipenv-pipes

Compatibility
^^^^^^^^^^^^

* Python 3.4+ (PRs for 2.7 welcome)
* Unix + Windows Support 💖


Usage
--------

List Pipenv Environments
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: bash

  $ pipes
  or
  $ pipes --list

.. code:: bash

  [ Pipenv Environments ]
    0: project1-LwEMcb8W *
    1: project2-R1v7_ynT *


The `*` indicates the Environment has a project directory associated.

*The lack of a* `*`, indicates the Environment has not yet been associated with a project directory.
If you try switching into an environment without the `*`, Pipes will tell you need to *link* the environment
with a project directory first.

To understand how Pipes links Project Directories with corresponding virtualenvs see `Link Environment to Project Directory`_.

To see a detail output of the detected pipenv enviroments and the maped project directories use the ``--verbose`` option:

.. code:: bash

    $ pipes --list -verbose

.. code:: bash


    PIPENV_HOME: /Users/username/.local/share/virtualenvs
    
    [ Pipenv Environments ]
    
      0: project1-LwEMcb8W
         Environment: /Users/username/.local/share/virtualenvs/project1-LwEMcb8W
         Project Dir: /Users/username/dev/project1
         
      1: project2-R1v7_ynT
         Environment: /Users/username/.local/share/virtualenvs/project2-R1v7_ynT
         Project Dir: /Users/username/dev/project2
    

*Project Dir* will show as `Not Set` if the Environment has not been associated with a Project directory.


Link Environment to Project Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you can switch into a project using Pipes, the selected environment must have a project directory associated with it.

To link a project directory with its environment use the ``--link`` flag:

.. code:: bash

    $ pipes --link /path/to/project1

Pipes will find the associated Pipenv Environmnet by running ``pipenv --venv`` from from the target directory.
Once detected, the project directory path is stored in the pipenv environemnt in a ``.project`` file.


Go To a Project by Name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once our Pipenv Enviromnents are asscociated with Project Directories,
we can use pipes to navigate our projects:

.. code:: bash

    $ pipes project1

This would cd into directory ``/path/to/project1`` and the corresponding Pipenv Shell is activated.

If query term (eg. ``project1``) returns two or more matches, Pipes will tell you that a more specific query term needs to be used.

For instance, to match ``0: project1-LwEMcb8W`` user would need to type ``project1`` to get a single match.
If query argument was ``project`` activation would fail since Pipes cannot guess which enviroment users wants 
(``project1`` or ``project2``).


Go To a Project by Index
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The environment index can also be used to switch into a project.
To active the enviroment ``1: project2-R1v7_ynT`` run:

.. code:: bash

    $ pipes 1:



Unlink a Project
^^^^^^^^^^^^^^^^^

To unlink ``project1`` directory from its Pipenv Enviroment run:

.. code:: bash

    $ pipes --unlink project1


Command Help
^^^^^^^^^^^^

For more details check ``pipes --help``


Known Issues
------------

* ``PIPENV_VENV_IN_PROJECT`` is not currently supported


License
-------

`MIT License <https://github.com/gtalarico/pipenv-pipes/blob/master/LICENSE>`_


Credits
-------

Inpired by `virtualenvwrapper`_

Package created with `Cookiecutter`_ + `cookiecutter-pypackage`_

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`virtualenvwrapper`: https://virtualenvwrapper.readthedocs.io/en/latest/


Author
------

Send me a message on `twitter`_

.. _`twitter`: https://twitter.com/gtalarico
