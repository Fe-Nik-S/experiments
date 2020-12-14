
import os
from utils import get_files_by_extension


def main():
    path_to_files = os.path.dirname(os.path.abspath(__file__))
    images = get_files_by_extension(path_to_files)
    print(images)


if __name__ == "__main__":
    main()