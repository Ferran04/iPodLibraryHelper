# file_processor/tests/test_scalability.py

import time
import os
import shutil
from processor import FileProcessor
from converters import FLACToAACConversion


def create_large_test_files(num_files):
    """Create a large number of test files."""
    if not os.path.exists('test_input'):
        os.makedirs('test_input')
    for i in range(num_files):
        with open(f'test_input/file_{i}.flac', 'w') as f:
            f.write("Dummy FLAC file content")


def test_scalability():
    """Test scalability with increasing number of files."""
    num_files_list = [10, 50, 100, 200, 500]  # Adjust numbers based on requirements

    for num_files in num_files_list:
        create_large_test_files(num_files)
        processor = FileProcessor('test_output', FLACToAACConversion())

        start_time = time.time()
        processor.get_flac_files_info('test_input')
        processor.process_files()
        end_time = time.time()

        processing_time = end_time - start_time
        print(f"Time taken for processing {num_files} files: {processing_time} seconds")

        shutil.rmtree('test_input')
        shutil.rmtree('test_output')


if __name__ == '__main__':
    test_scalability()
