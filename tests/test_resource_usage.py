# file_processor/tests/test_resource_usage.py

import psutil
import time
from processor import FileProcessor
from converters import FLACToAACConversion


def monitor_resource_usage():
    """Monitor resource usage during file processing."""
    cpu_before = psutil.cpu_percent(interval=1)
    mem_before = psutil.virtual_memory().percent

    # Initialize FileProcessor with a conversion strategy
    processor = FileProcessor('test_output', FLACToAACConversion())

    start_time = time.time()
    processor.get_flac_files_info('test_input')
    processor.process_files()
    end_time = time.time()

    cpu_after = psutil.cpu_percent(interval=1)
    mem_after = psutil.virtual_memory().percent

    print(f"CPU usage before: {cpu_before}%")
    print(f"CPU usage after: {cpu_after}%")
    print(f"Memory usage before: {mem_before}%")
    print(f"Memory usage after: {mem_after}%")


if __name__ == '__main__':
    monitor_resource_usage()
