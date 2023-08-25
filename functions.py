from constants import TRANS
from pathlib import Path
import shutil


CATEGORIES = dict()


with open('categories.txt') as fh:
    contents = fh.read()
    lines = contents.strip().split("\n")
    for line in lines:
        key_value = line.split(":")
        key = key_value[0].strip()
        values_str = key_value[1].strip()
        values = values_str.split(",")
        values = [value.strip() for value in values]
        if not values_str:
            CATEGORIES[key] = None
        CATEGORIES[key] = values


def normalize(name: str) -> str:
    return name.translate(TRANS)


def create_folders(directory):
    for folder_name in CATEGORIES.keys():
        try:
            new_folder = directory / folder_name
            new_folder.mkdir()
        except FileExistsError:
            print(f'Folder named {folder_name} already exists.')


def find_replace(directory: Path, file: Path):
    for category, extensions in CATEGORIES.items():
        new_path = directory / category
        if not extensions:
            file.replace(new_path / normalize(file.name))
            return None
        if file.suffix.lower() in extensions:
            file.replace(new_path / normalize(file.name))
            return None

    return None


def replace_files(directory: Path):
    for file in directory.glob('**/*.*'):
        find_replace(directory, file)


def unpack_archive(directory: Path):
    archive_directory = directory / 'ARCHIVES'
    for archive in archive_directory.glob('*.*'):
        path_archive_folder = archive_directory / archive.stem.upper()
        shutil.unpack_archive(archive, path_archive_folder)


def delete_empty_folders(directory: Path):
    empty_folders = []
    for folder in directory.glob('**/*'):
        if folder.is_dir() and not any(folder.iterdir()):
            empty_folders.append(folder)

    for folder in empty_folders:
        shutil.rmtree(str(folder))
        print(f'{folder.name} folder deleted.')
