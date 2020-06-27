import os


def create_folder(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
