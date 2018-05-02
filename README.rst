============
Pipes - Pipenv Environment Switcher
============


.. image:: https://img.shields.io/pypi/v/pipenv_pipes.svg
        :target: https://pypi.python.org/pypi/pipenv_pipes

.. image:: https://img.shields.io/travis/gtalarico/pipenv_pipes.svg
        :target: https://travis-ci.org/gtalarico/pipenv_pipes

.. image:: https://readthedocs.org/projects/pipenv-pipes/badge/?version=latest
        :target: https://pipenv-pipes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




CLI tool to speed up navigating your Pipenv Enviroments and the corresponding Project Directories.

The goal of Pipes is to provide a pipenv equivalent of the ``workon`` tool provided by virtualenvwrapper.


* Documentation: https://pipenv-pipes.readthedocs.io.
* Free software: MIT license


Install
--------

``pip install pipenv-pipes``

Usage
--------

* Show Available Pipenv Environments

``pipes list``

* Link Project Directory to Pipenv Environment (this adds a .project file to your environment folder)

``pipes set projectname /path/to/project``

* Go to directory and Activate Pipenv Shell

``pipes go projectname``

Todo
-------

* Simplify CLI Api (pipes only)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
