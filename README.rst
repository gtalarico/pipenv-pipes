============
Pipenv Pipes
============


.. image:: https://img.shields.io/pypi/v/pipenv_pipes.svg
        :target: https://pypi.python.org/pypi/pipenv_pipes

.. image:: https://img.shields.io/travis/gtalarico/pipenv_pipes.svg
        :target: https://travis-ci.org/gtalarico/pipenv_pipes

.. image:: https://readthedocs.org/projects/pipenv-pipes/badge/?version=latest
        :target: https://pipenv-pipes.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




CLI Tool to help manage Pipenv Enviroments and corresponding Project Directories.


* Free software: MIT license
* Documentation: https://pipenv-pipes.readthedocs.io.


Install
--------

``pip install pipenv-pipes``

Usage
--------

* List Pipenv Environments

``pipes list``

* Add Project Directory to Pipenv Environment

``pipes set projectname /path/to/project``

* Activate Pipenv Environments and Go to directory

``pipes go projectname``

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
