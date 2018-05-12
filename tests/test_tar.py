import tarfile
import os
# from .utils import make_tarfile, unzip_tar


def make_tarfile(src_dir, dst):
    with tarfile.open(dst, "w:gz") as tar:
        tar.add(src_dir, arcname=os.path.basename(src_dir))


def unzip_tar(src, dst):
    with tarfile.open(src, "r:gz") as tar:
        tar.extractall(path=dst)


def test_unzip(venv_archive_path, temp_folder):
    unzip_tar(src=venv_archive_path, dst=temp_folder)
    tarname = os.path.basename(venv_archive_path)
    tarpath = os.path.join(temp_folder, tarname)
    assert os.listdir(temp_folder)
