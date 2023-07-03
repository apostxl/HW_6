from functions import create_folders, replace_files,\
    unpack_archive, delete_empty_folders
from pathlib import Path
from sys import argv
from constants import TRANS
from pathlib import Path
import shutil
from string import punctuation


def print_in_cmd(directory):
    for folder in directory.glob('*'):
        files_name = [file.name for file in folder.iterdir() if file.is_file()]
        files_ext = set(file.suffix for file in folder.iterdir()
                        if file.is_file())

        print(f'Files names in {folder.name}: \n{files_name}')
        print(f'Files extensions in {folder.name}: \n{files_ext}')
        print('_' * 30)


def main():
    user_input = input(
        f'Are you sure you want to sort files in "{argv[1]}" ?(y/n): ').lower()

    match user_input:
        case 'n':
            print('The programm was stopped by user.')
        case 'y':
            try:
                directory = Path(argv[1])
            except IndexError:
                print('Must be path to folder')
            if not directory.exists():
                print("The folder doesn't exist")
            else:
                create_folders(directory)
                replace_files(directory)
                unpack_archive(directory)
                delete_empty_folders(directory)
                print_in_cmd(directory)

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


if __name__ == '__main__':
    main()

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = (
    'a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
    'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu',
    'ya', 'je', 'i', 'ji', 'g'
)
PROBLEM_SYMBOLS = punctuation.replace('.', ' ')
TRANS = {}

for cyrillic, translation in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = translation
    TRANS[ord(cyrillic.upper())] = translation.upper()

for symbol in PROBLEM_SYMBOLS:
    TRANS[ord(symbol)] = "_"
