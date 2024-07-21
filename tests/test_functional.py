import unittest
from unittest.mock import patch, MagicMock
from processor import FileProcessor
from converters import FLACToAACConversion, FLACToWAVConversion
import os


class TestFileProcessorFunctional(unittest.TestCase):

    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['test_file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    @patch('builtins.input', side_effect=['1', 'E:\\1. IPOD LIBRARY\\256 AAC'])
    @patch('file_processor.processor.os.makedirs')
    @patch('file_processor.processor.os.remove')
    def test_process_files_valid(self, mock_remove, mock_makedirs, mock_input, mock_convert, mock_remove_cover_image,
                                 mock_listdir, mock_get_metadata):
        """Test the FileProcessor with valid input and FLAC to AAC conversion."""
        processor = FileProcessor('E:\\1. IPOD LIBRARY\\256 AAC', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        mock_convert.assert_called_once_with('test_file.flac', 'target_dir\\00. Test Metadata.m4a')
        mock_remove_cover_image.assert_called_once()
        mock_listdir.assert_called_once()

    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['test_file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    @patch('builtins.input', side_effect=['2', 'E:\\1. IPOD LIBRARY\\WAV'])
    @patch('file_processor.processor.os.makedirs')
    @patch('file_processor.processor.os.remove')
    def test_process_files_valid_wav(self, mock_remove, mock_makedirs, mock_input, mock_convert,
                                     mock_remove_cover_image, mock_listdir, mock_get_metadata):
        """Test the FileProcessor with valid input and FLAC to WAV conversion."""
        processor = FileProcessor('E:\\1. IPOD LIBRARY\\WAV', FLACToWAVConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        mock_convert.assert_called_once_with('test_file.flac', 'target_dir\\00. Test Metadata.wav')
        mock_remove_cover_image.assert_called_once()
        mock_listdir.assert_called_once()

    @patch('builtins.input', side_effect=['3', 'E:\\1. IPOD LIBRARY\\256 AAC'])
    def test_invalid_conversion_choice(self, mock_input):
        """Test invalid conversion choice in the user input."""
        with self.assertRaises(ValueError):
            from ..main import get_conversion_strategy
            get_conversion_strategy()

    @patch('builtins.input', side_effect=['1', 'InvalidPath'])
    @patch('file_processor.processor.os.path.isdir', return_value=False)
    def test_invalid_directory_path(self, mock_isdir, mock_input):
        """Test invalid directory path input."""
        with self.assertRaises(ValueError):
            from ..processor import FileProcessor
            processor = FileProcessor('InvalidPath', FLACToAACConversion())
            processor.input_directory()

    @patch('file_processor.processor.os.path.isdir', return_value=True)
    @patch('builtins.input', side_effect=['1', 'E:\\1. IPOD LIBRARY\\256 AAC'])
    @patch('file_processor.processor.os.listdir', return_value=[])
    def test_no_flac_files(self, mock_listdir, mock_input, mock_isdir):
        """Test the scenario where no FLAC files are found in the directory."""
        processor = FileProcessor('E:\\1. IPOD LIBRARY\\256 AAC', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        # No FLAC files should result in no conversion calls
        assert processor.converter.strategy.convert.call_count == 0


if __name__ == '__main__':
    unittest.main()
