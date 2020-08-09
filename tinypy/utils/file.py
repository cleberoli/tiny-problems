import os
import shutil

MAIN_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def create_directory(path: str):
    """Creates the directory if it doesn't exist.

    Args:
        path: The directory path.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_full_path(*path):
    """Returns the given path joined by the MAIN_DIRECTORY.

    Args:
        *path: The path.
    """
    return os.path.join(MAIN_DIRECTORY, *path)


def file_exists(path: str):
    """Checks whether a file exists.

    Args:
        path: The path.
    """
    return os.path.exists(path)


def delete_directory(path: str):
    """Deletes the directory recursively.

    Args:
        path: The path.
    """
    shutil.rmtree(path)


def delete_directory_files(path: str, prefix: str):
    """Deletes all files in the given path if they start with the given prefix.

    Args:
        path: The path.
        prefix: The prefix.
    """
    for f_name in os.listdir(path):
        if f_name.startswith(prefix):
            os.remove(os.path.join(path, f_name))


def delete_file(path: str):
    """Deletes the file.

    Args:
        path: The path.
    """
    os.remove(path)
