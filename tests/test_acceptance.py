# file_processor/tests/test_acceptance.py

import unittest
import os
import subprocess
from unittest.mock import patch, MagicMock
from processor import FileProcessor
from converters import FLACToAACConversion, FLACToWAVConversion


class TestFileProcessorAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'test_dir'
        cls.flac_file = os.path.join(cls.test_dir, 'test.flac')
        cls.aac_file = os.path.join(cls.test_dir, 'test.m4a')

        # Create test directory and FLAC file
        os.makedirs(cls.test_dir, exist_ok=True)
        with open(cls.flac_file, 'wb') as f:
            f.write(b'\x00')  # Dummy content

    @classmethod
    def tearDownClass(cls):
        # Cleanup
        if os.path.exists(cls.flac_file):
            os.remove(cls.flac_file)
        if os.path.exists(cls.aac_file):
            os.remove(cls.aac_file)
        if os.path.exists(cls.test_dir):
            os.rmdir(cls.test_dir)

    @patch('file_processor.processor.Converter.convert')
    def test_flac_to_aac_conversion(self, mock_convert):
        mock_convert.return_value = None  # Mock the conversion to avoid actual file conversion

        processor = FileProcessor(self.test_dir, FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value=self.test_dir)

        processor.process_files()

        # Verify conversion was called
        mock_convert.assert_called_once_with(self.flac_file, os.path.join(self.test_dir, '01. Unknown Title'))

        # Check that original FLAC file is deleted
        self.assertFalse(os.path.exists(self.flac_file))

        # Check that AAC file exists
        self.assertTrue(os.path.exists(self.aac_file))

    @patch('file_processor.processor.Converter.convert')
    def test_flac_to_wav_conversion(self, mock_convert):
        mock_convert.return_value = None  # Mock the conversion to avoid actual file conversion

        processor = FileProcessor(self.test_dir, FLACToWAVConversion())
        processor.create_directory_structure = MagicMock(return_value=self.test_dir)

        processor.process_files()

        # Verify conversion was called
        mock_convert.assert_called_once_with(self.flac_file, os.path.join(self.test_dir, '01. Unknown Title'))

        # Check that original FLAC file is deleted
        self.assertFalse(os.path.exists(self.flac_file))

        # Check that WAV file does not exist (since it should have been replaced by the AAC file in this case)
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, '01. Unknown Title.wav')))

    @patch('builtins.input', side_effect=['2', 'test_dir'])
    @patch('file_processor.processor.FileProcessor.input_directory', return_value='test_dir')
    @patch('file_processor.processor.FileProcessor.process_files')
    def test_invalid_directory(self, mock_process_files, mock_input_directory, mock_input):
        processor = FileProcessor(self.test_dir, FLACToWAVConversion())
        processor.create_directory_structure = MagicMock(return_value=self.test_dir)

        processor.process_files()

        # Ensure process_files method is called
        mock_process_files.assert_called_once()

        # Check for user input and directory handling
        mock_input.assert_called_with("Please enter the source directory you want to work with\n")


if __name__ == '__main__':
    unittest.main()
