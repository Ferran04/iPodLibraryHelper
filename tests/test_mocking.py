# file_processor/tests/test_mocking.py

import unittest
from unittest.mock import patch, MagicMock
from processor import FileProcessor
from converters import FLACToAACConversion, FLACToWAVConversion
import subprocess


class TestFileProcessorMocking(unittest.TestCase):

    @patch('file_processor.processor.subprocess.run')
    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    def test_conversion_success(self, mock_remove_cover_image, mock_listdir, mock_get_metadata, mock_subprocess):
        # Simulate successful subprocess call
        mock_subprocess.return_value = None

        processor = FileProcessor('test_dir', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        # Check if subprocess.run was called with the correct arguments
        mock_subprocess.assert_called_once_with([
            'ffmpeg', '-i', 'file.flac',
            '-c:a', 'aac', '-b:a', '256k',
            '-aac_pns', '0', '-ar', '44100',
            'target_dir/00. Test Title.m4a'
        ], check=True)

    @patch('file_processor.processor.subprocess.run')
    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    def test_conversion_failure(self, mock_remove_cover_image, mock_listdir, mock_get_metadata, mock_subprocess):
        # Simulate failed subprocess call
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'ffmpeg')

        processor = FileProcessor('test_dir', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')

        with self.assertLogs('file_processor.processor', level='ERROR') as log:
            processor.process_files()
            self.assertIn('Conversion error for file.flac:', log.output[0])

    @patch('file_processor.processor.subprocess.run')
    def test_converter_with_stub(self, mock_subprocess):
        # Stub the Converter to do nothing during tests
        stub_converter = MagicMock()
        processor = FileProcessor('test_dir', stub_converter)

        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.get_flac_files_info = MagicMock(
            return_value=[{'file': 'file.flac', 'title': 'Test Title', 'track_number': '01'}])

        processor.process_files()

        # Check if the stubbed convert method was called
        stub_converter.convert.assert_called_once_with('file.flac', 'target_dir/01. Test Title')


if __name__ == '__main__':
    unittest.main()
