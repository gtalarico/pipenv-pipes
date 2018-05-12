""" This is only to test the pytest --profile pluging failure documented
here: https://github.com/manahl/pytest-plugins/issues/40
"""

import pytest # noqa
import os
from tempfile import TemporaryDirectory


@pytest.fixture
def tempdir():
    _cwd = os.getcwd()
    with TemporaryDirectory() as path:
        os.chdir(path)
        os.makedirs('folder')
        folderpath = os.path.join(os.getcwd(), 'folder')
        yield folderpath

    os.chdir(_cwd)


def test_chdir(tempdir):
    assert os.path.exists(tempdir)
