import os
import logging
from collections import namedtuple

logging.basicConfig(filename='directory_info.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_dir', 'parent'])


def get_directory_info(directory_path):
    directory_contents = []

    for root, dirs, files in os.walk(directory_path):
        parent_dir = os.path.basename(root)

        for dir_name in dirs:
            info = FileInfo(name=dir_name, extension='', is_dir=True, parent=parent_dir)
            directory_contents.append(info)
            logging.info(f"Directory: {info}")

        for file_name in files:
            name, extension = os.path.splitext(file_name)
            info = FileInfo(name=name, extension=extension, is_dir=False, parent=parent_dir)
            directory_contents.append(info)
            logging.info(f"File: {info}")

    return directory_contents


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print(f"The path {directory_path} is not a valid directory.")
        sys.exit(1)

    directory_info = get_directory_info(directory_path)
    for info in directory_info:
        print(info)
