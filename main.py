# file_processor/main.py

import os

from converters import FLACToAACConversion, FLACToWAVConversion, ConversionStrategy
from processor import FileProcessor


def main():
    conversion_strategy = get_conversion_strategy()
    dir_library = get_directory_path(conversion_strategy)
    processor = FileProcessor(dir_library, conversion_strategy)
    processor.process_files()


def get_conversion_strategy() -> ConversionStrategy:
    print("Select conversion type:")
    print("1. FLAC to 256 AAC")
    print("2. FLAC to WAV")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        return FLACToAACConversion()
    elif choice == '2':
        return FLACToWAVConversion()
    else:
        raise ValueError("Invalid choice. Please select 1 or 2.")


def get_directory_path(strategy: ConversionStrategy) -> str:
    base_dir = 'E:\\1. IPOD LIBRARY'  # Base directory can be a constant or dynamically set
    if isinstance(strategy, FLACToAACConversion):
        return os.path.join(base_dir, '256 AAC')
    elif isinstance(strategy, FLACToWAVConversion):
        return os.path.join(base_dir, 'WAV')
    else:
        raise ValueError("Unsupported conversion strategy")


if __name__ == '__main__':
    main()
