# file_processor/tests/test_integration.py

import unittest
from unittest.mock import patch, MagicMock
import os
from processor import FileProcessor
from converters import FLACToAACConversion, FLACToWAVConversion


class TestFileProcessorIntegration(unittest.TestCase):

    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    def test_process_files_with_aac_conversion(self, mock_convert, mock_remove_cover_image, mock_listdir,
                                               mock_get_metadata):
        # Setup
        mock_convert.return_value = None
        mock_remove_cover_image.return_value = None

        # Instantiate FileProcessor with FLACToAACConversion
        processor = FileProcessor('test_dir', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')

        # Execute the process
        processor.process_files()

        # Assert that conversion was called once
        mock_convert.assert_called_once()
        # Assert that remove_cover_image was called once
        mock_remove_cover_image.assert_called_once()
        # Assert that directory creation was mocked properly
        processor.create_directory_structure.assert_called_once_with('Unknown Artist', 'Unknown Album', 'Unknown Date')

    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    def test_process_files_with_wav_conversion(self, mock_convert, mock_remove_cover_image, mock_listdir,
                                               mock_get_metadata):
        # Setup
        mock_convert.return_value = None
        mock_remove_cover_image.return_value = None

        # Instantiate FileProcessor with FLACToWAVConversion
        processor = FileProcessor('test_dir', FLACToWAVConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')

        # Execute the process
        processor.process_files()

        # Assert that conversion was called once
        mock_convert.assert_called_once()
        # Assert that remove_cover_image was called once
        mock_remove_cover_image.assert_called_once()
        # Assert that directory creation was mocked properly
        processor.create_directory_structure.assert_called_once_with('Unknown Artist', 'Unknown Album', 'Unknown Date')

    @patch('file_processor.processor.FileUtils.is_windows_directory_format', return_value=True)
    @patch('builtins.input', side_effect=['E:\\1. IPOD LIBRARY', '1'])
    @patch('file_processor.processor.FileProcessor.process_files')
    def test_main_function_integration(self, mock_process_files, mock_input, mock_is_windows_directory_format):
        from ..main import main

        # Mocking to simulate user input and valid directory format
        with patch('file_processor.main.get_conversion_strategy', return_value=FLACToAACConversion()):
            with patch('file_processor.main.get_directory_path', return_value='test_dir'):
                main()

        # Check that process_files was called in the main function
        mock_process_files.assert_called_once()


if __name__ == '__main__':
    unittest.main()
