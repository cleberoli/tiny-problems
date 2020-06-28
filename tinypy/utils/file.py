import os

MAIN_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def create_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def get_full_path(*path):
    return os.path.join(MAIN_DIRECTORY, *path)

