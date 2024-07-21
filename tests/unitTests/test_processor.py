# file_processor/tests/test_processor.py

import unittest
from unittest.mock import patch, MagicMock
from processor import FileProcessor
from converters import ConversionStrategy
from utils import FileUtils


class TestFileProcessor(unittest.TestCase):
    @patch('file_processor.processor.os')
    @patch('file_processor.processor.FileUtils')
    @patch('file_processor.processor.FLAC')
    @patch('file_processor.processor.Converter')
    def setUp(self, MockConverter, MockFLAC, MockUtils, MockOS):
        self.mock_converter = MockConverter.return_value
        self.mock_utils = MockUtils
        self.mock_flac = MockFLAC
        self.mock_os = MockOS
        self.processor = FileProcessor('dummy_dir', MagicMock())

    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    def test_get_flac_files_info(self, mock_remove_cover_image, mock_listdir, mock_get_metadata):
        self.processor.extract_flac_metadata = MagicMock(return_value={'title': 'Test Title'})
        result = self.processor.get_flac_files_info('dummy_dir')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Title')

    @patch('file_processor.processor.input', return_value='dummy_dir')
    @patch('file_processor.processor.os.path.isdir', return_value=True)
    def test_input_directory(self, mock_isdir, mock_input):
        directory = self.processor.input_directory()
        self.assertEqual(directory, 'dummy_dir')

    @patch('file_processor.processor.FileProcessor.get_flac_files_info', return_value=[{'file': 'file.flac'}])
    @patch('file_processor.processor.FileProcessor.create_directory_structure', return_value='target_dir')
    @patch('file_processor.processor.tqdm')
    def test_process_files(self, mock_tqdm, mock_create_directory_structure, mock_get_flac_files_info):
        with patch('file_processor.processor.os.remove') as mock_remove:
            self.processor.process_files()
            mock_remove.assert_called_once_with('file.flac')
            self.mock_converter.convert.assert_called_once()


if __name__ == '__main__':
    unittest.main()
