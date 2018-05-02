============
Pipes - Pipenv Environment Switcher
============


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




CLI tool to speed up navigating your Pipenv Enviroments and the corresponding Project Directories.

The goal of Pipes is to provide a pipenv equivalent of the ``workon`` tool provided by virtualenvwrapper.


* Documentation: https://pipenv-pipes.readthedocs.io.
* Free software: MIT license


Install
--------

``pip install pipenv-pipes``

Usage
--------

Show Available Pipenv Environments

``pipes``

Link Project Directory to Pipenv Environment (this adds a .project file to your environment folder)

``pipes envname --set /path/to/project``

Go to directory and Activate Pipenv Enviroment Shell

``pipes envname``

For more details check ``pipes --help``


Todo
-------

* Add cd-only flag (don't activate shell)
* Add tests + Contributing
* Setup Travis CI + Code Cov
* Add Documentation


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
