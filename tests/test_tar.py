import os
import tarfile
from conftest import unzip_tar


def make_tarfile(src_dir, dst):
    with tarfile.open(dst, "w:gz") as tar:
        tar.add(src_dir, arcname=os.path.basename(src_dir))


def test_unzip(venv_archive_path, temp_folder):
    unzip_tar(src=venv_archive_path, dst=temp_folder)
    assert os.listdir(temp_folder)
