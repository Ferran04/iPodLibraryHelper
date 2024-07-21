import os
import shutil
import unittest
from unittest.mock import patch, MagicMock
from processor import FileProcessor
from converters import FLACToAACConversion, FLACToWAVConversion


class TestFileProcessorE2E(unittest.TestCase):
    test_dir = 'test_e2e_dir'
    test_flac_file = 'test.flac'
    converted_file_aac = 'test.m4a'
    converted_file_wav = 'test.wav'

    @classmethod
    def setUpClass(cls):
        # Create a test directory and a test FLAC file
        if not os.path.exists(cls.test_dir):
            os.makedirs(cls.test_dir)

        with open(os.path.join(cls.test_dir, cls.test_flac_file), 'w') as f:
            f.write("This is a test FLAC file.")

    @classmethod
    def tearDownClass(cls):
        # Clean up the test directory
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def test_conversion_to_aac(self):
        with patch('file_processor.processor.get_conversion_strategy', return_value=FLACToAACConversion()):
            with patch('file_processor.processor.get_directory_path', return_value=self.test_dir):
                processor = FileProcessor(self.test_dir, FLACToAACConversion())
                processor.create_directory_structure = MagicMock(return_value=self.test_dir)
                processor.process_files()

                # Check if the AAC file is created
                self.assertTrue(os.path.exists(os.path.join(self.test_dir, self.converted_file_aac)))
                # Optionally, you can check the content of the AAC file if needed

    def test_conversion_to_wav(self):
        with patch('file_processor.processor.get_conversion_strategy', return_value=FLACToWAVConversion()):
            with patch('file_processor.processor.get_directory_path', return_value=self.test_dir):
                processor = FileProcessor(self.test_dir, FLACToWAVConversion())
                processor.create_directory_structure = MagicMock(return_value=self.test_dir)
                processor.process_files()

                # Check if the WAV file is created
                self.assertTrue(os.path.exists(os.path.join(self.test_dir, self.converted_file_wav)))
                # Optionally, you can check the content of the WAV file if needed

    def test_invalid_directory(self):
        with patch('builtins.input', side_effect=['invalid_dir']):
            with patch('file_processor.processor.FileUtils.is_windows_directory_format', return_value=False):
                processor = FileProcessor(self.test_dir, FLACToAACConversion())
                directory = processor.input_directory()

                # Ensure that the input directory is requested again after invalid input
                self.assertEqual(directory, 'invalid_dir')

                # Simulate valid directory input
                with patch('builtins.input', return_value=self.test_dir):
                    directory = processor.input_directory()
                    self.assertEqual(directory, self.test_dir)


if __name__ == '__main__':
    unittest.main()
