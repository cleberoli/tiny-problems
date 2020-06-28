import os
import shutil

MAIN_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def create_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def get_full_path(*path):
    return os.path.join(MAIN_DIRECTORY, *path)


def file_exists(path: str):
    return os.path.exists(path)


def delete_directory(path: str):
    shutil.rmtree(path)

