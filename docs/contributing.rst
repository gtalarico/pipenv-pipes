.. highlight:: console

============
Contributing
============

Contributions are welcome and greatly appreciated!
Every little bit helps, and credit will always be given.

-----------------------------------------------------------------------

How to Contribute
-----------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/gtalarico/pipenv-pipes/issues.


Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.


Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.


Write Documentation
~~~~~~~~~~~~~~~~~~~

Pipenv Pipes could always use more documentation, whether as part of the
official Pipenv Pipes docs, in docstrings, or even on the web in blog posts,
articles, and such.


Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/gtalarico/pipenv-pipes/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome.

------------------------------------------------------------

Setup Pipes Development Environment
-----------------------------------

Ready to contribute?
Here's how to set up Pipes for local development.

1. Fork the the Pipes repository from `GitHub`_.

.. _Github: https://github.com/gtalarico/pipenv-pipes#fork-destination-box


2. Clone your fork locally:

.. code:: console

    $ git clone git@github.com:YOUR_GITHUB_USERNAME/pipenv_pipes.git


3. Create a virtualenvironment - we will use Pipenv:

.. code:: console

    $ cd pipenv_pipes
    $ pipenv install --dev
    $ python setup.py develop

4. Create a branch for local development so you can make your changes locally:

.. code:: console

  $ git checkout -b name-of-your-bugfix-or-feature


5. When you're done making changes, check that your changes pass all tests. See the `Testing`_ section below for more details on testing.

6. Commit your changes and push your branch to GitHub:

.. code:: console

  $ git add .
  $ git commit -m "Your detailed description of your changes."
  $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.


-----------------------------------------

Testing
-------

Run test suite
~~~~~~~~~~~~~~

Tests use Pytest. To run the test suite run:

.. code:: console

  $ pytest
  or
  $ python setup.py test or

Linter
~~~~~~

Make sure the code follows Flake 8 standard by using a linter within your code
editor or use the command below:

.. code:: console

  $ flake8 pipenv_pipes tests


Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.4, 3.5 and 3.6, and for PyPy. Check
   https://travis-ci.org/gtalarico/pipenv_pipes/pull_requests
   and make sure that the tests pass for all supported Python versions.


Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run:

.. code:: console

  $ bump2version  major / minor / patch / release
  $ git push
  $ git push --tags

.. note::

  Travis should run all tests but integration with PyPI is currently disabled.
  To deploy to Pypi use ``make release``.
