import os

from tinypy.utils.file import create_directory, get_full_path, file_exists, delete_directory, delete_directory_files, delete_file


def test_create_directory():
    path = get_full_path('files', 'misc')
    assert not os.path.exists(path)

    create_directory(path)
    assert os.path.exists(path)

    os.rmdir(path)
    assert not os.path.exists(path)


def test_get_full_path():
    current_path = os.path.dirname(__file__).split('\\')

    path = current_path[:-3]
    assert get_full_path().split('\\') == path

    path.append('misc')
    assert get_full_path('misc').split('\\') == path


def test_file_exists():
    path = get_full_path('files', 'misc')
    file = get_full_path('files', 'misc', 'file.txt')

    assert not file_exists(path)
    assert not file_exists(file)

    os.makedirs(path)
    with open(file, 'w+') as f:
        f.write('')

    assert file_exists(path)
    assert file_exists(file)

    os.remove(file)
    os.rmdir(path)

    assert not file_exists(path)
    assert not file_exists(file)


def test_delete_directory():
    path = get_full_path('files', 'misc')
    f1 = get_full_path('files', 'misc', 'file1.txt')
    f2 = get_full_path('files', 'misc', 'file2.txt')
    f3 = get_full_path('files', 'misc', '3file.txt')

    assert not os.path.exists(path)
    assert not os.path.exists(f1)
    assert not os.path.exists(f2)
    assert not os.path.exists(f3)

    os.makedirs(path)
    with open(f1, 'w+') as file:
        file.write('')
    with open(f2, 'w+') as file:
        file.write('')
    with open(f3, 'w+') as file:
        file.write('')

    assert os.path.exists(path)
    assert os.path.exists(f1)
    assert os.path.exists(f2)
    assert os.path.exists(f3)

    delete_directory(path)

    assert not os.path.exists(path)
    assert not os.path.exists(f1)
    assert not os.path.exists(f2)
    assert not os.path.exists(f3)


def test_delete_directory_files():
    path = get_full_path('files', 'misc')
    f1 = get_full_path('files', 'misc', 'file1.txt')
    f2 = get_full_path('files', 'misc', 'file2.txt')
    f3 = get_full_path('files', 'misc', '3file.txt')

    assert not os.path.exists(path)
    assert not os.path.exists(f1)
    assert not os.path.exists(f2)
    assert not os.path.exists(f3)

    os.makedirs(path)
    with open(f1, 'w+') as file:
        file.write('')
    with open(f2, 'w+') as file:
        file.write('')
    with open(f3, 'w+') as file:
        file.write('')

    assert os.path.exists(path)
    assert os.path.exists(f1)
    assert os.path.exists(f2)
    assert os.path.exists(f3)

    delete_directory_files(path, 'file')

    assert os.path.exists(path)
    assert not os.path.exists(f1)
    assert not os.path.exists(f2)
    assert os.path.exists(f3)

    delete_directory(path)


def test_delete_file():
    path = get_full_path('files', 'misc')
    file = get_full_path('files', 'misc', 'file.txt')

    assert not file_exists(path)
    assert not file_exists(file)

    os.makedirs(path)
    with open(file, 'w+') as f:
        f.write('')

    assert file_exists(path)
    assert file_exists(file)

    delete_file(file)
    assert not file_exists(file)

    delete_directory(path)
    assert not file_exists(path)
