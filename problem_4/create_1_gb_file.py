import os
from os.path import exists

from config import settings


def create_1_gb_file():
    """Create test file with the size of 1Gb."""
    if not exists(settings.TEST_FILE):
        file_size = 1024 * 1024 * 1024
        with open(settings.TEST_FILE, 'wb') as file:
            while os.path.getsize(settings.TEST_FILE) < file_size:
                block_size = min(8192, file_size - file.tell())
                block = b'\x00' * block_size
                file.write(block)
        return '1Gb file created'
    return 'File has been created already'


if __name__ == '__main__':
    print(create_1_gb_file())
