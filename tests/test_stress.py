# file_processor/tests/test_stress.py

import os
import shutil
from processor import FileProcessor
from converters import FLACToAACConversion


def create_large_file(file_name, size_mb):
    """Create a large test file of specified size."""
    with open(file_name, 'wb') as f:
        f.write(b'\0' * (size_mb * 1024 * 1024))


def test_stress_large_file():
    """Test stress with large file size."""
    create_large_file('test_input/large_file.flac', 100)  # 100 MB file
    processor = FileProcessor('test_output', FLACToAACConversion())

    processor.get_flac_files_info('test_input')
    processor.process_files()

    shutil.rmtree('test_input')
    shutil.rmtree('test_output')


if __name__ == '__main__':
    test_stress_large_file()
