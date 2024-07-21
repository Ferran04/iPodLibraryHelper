# file_processor/tests/test_performance.py

import time
import os
import shutil
from processor import FileProcessor
from converters import FLACToAACConversion


def setup_test_environment():
    """Prepare test environment by creating test files and directories."""
    if not os.path.exists('test_input'):
        os.makedirs('test_input')
    # Create dummy FLAC files for testing
    for i in range(100):  # Adjust the number based on the load you want to test
        with open(f'test_input/file_{i}.flac', 'w') as f:
            f.write("Dummy FLAC file content")


def clean_up_test_environment():
    """Clean up test environment."""
    if os.path.exists('test_input'):
        shutil.rmtree('test_input')
    if os.path.exists('test_output'):
        shutil.rmtree('test_output')


def test_performance_file_processing():
    """Test performance of file processing with multiple files."""
    setup_test_environment()

    # Initialize FileProcessor with a conversion strategy
    processor = FileProcessor('test_output', FLACToAACConversion())

    start_time = time.time()
    processor.get_flac_files_info('test_input')  # This could be adapted based on how you want to test
    processor.process_files()
    end_time = time.time()

    processing_time = end_time - start_time
    print(f"Time taken for processing 100 files: {processing_time} seconds")

    clean_up_test_environment()


if __name__ == '__main__':
    test_performance_file_processing()
