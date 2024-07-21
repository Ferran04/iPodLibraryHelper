import unittest
from unittest.mock import patch, MagicMock
from processor import FileProcessor
from converters import FLACToAACConversion, FLACToWAVConversion
from mutagen.flac import FLAC
import os


class TestFileProcessorEdgeCases(unittest.TestCase):

    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['empty_file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    @patch('file_processor.processor.FLAC', autospec=True)
    def test_empty_flac_file(self, mock_flac, mock_convert, mock_remove_cover_image, mock_listdir, mock_get_metadata):
        """Test handling of an empty FLAC file."""
        mock_flac.return_value = MagicMock(spec=FLAC)
        mock_flac.return_value.pictures = []
        mock_flac.return_value.get.return_value = ['']  # Simulate empty file with empty metadata

        processor = FileProcessor('E:\\1. IPOD LIBRARY\\256 AAC', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        # Conversion should not be attempted for empty files
        mock_convert.assert_not_called()
        mock_remove_cover_image.assert_called_once()
        mock_listdir.assert_called_once()

    @patch('file_processor.processor.FileUtils.get_metadata', side_effect=Exception("Metadata retrieval error"))
    @patch('file_processor.processor.os.listdir', return_value=['valid_file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    @patch('file_processor.processor.FLAC', autospec=True)
    def test_flac_file_with_metadata_retrieval_error(self, mock_flac, mock_convert, mock_remove_cover_image,
                                                     mock_listdir, mock_get_metadata):
        """Test handling of FLAC files when metadata retrieval fails."""
        mock_flac.return_value = MagicMock(spec=FLAC)
        mock_flac.return_value.pictures = []

        processor = FileProcessor('E:\\1. IPOD LIBRARY\\256 AAC', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        # Conversion should not be attempted if metadata retrieval fails
        mock_convert.assert_not_called()
        mock_remove_cover_image.assert_called_once()
        mock_listdir.assert_called_once()

    @patch('file_processor.processor.FileUtils.get_metadata', return_value='Test Metadata')
    @patch('file_processor.processor.os.listdir', return_value=['unsupported_file.txt'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    def test_unsupported_file_format(self, mock_remove_cover_image, mock_listdir, mock_get_metadata, mock_convert):
        """Test handling of unsupported file formats."""
        processor = FileProcessor('E:\\1. IPOD LIBRARY\\256 AAC', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        # Conversion should not be attempted for unsupported file formats
        mock_convert.assert_not_called()
        mock_remove_cover_image.assert_not_called()
        mock_listdir.assert_called_once()

    @patch('file_processor.processor.FileUtils.get_metadata', return_value=None)  # Simulate None for missing metadata
    @patch('file_processor.processor.os.listdir', return_value=['missing_metadata_file.flac'])
    @patch('file_processor.processor.FileUtils.remove_cover_image')
    @patch('file_processor.processor.Converter.convert')
    @patch('file_processor.processor.FLAC', autospec=True)
    def test_missing_metadata(self, mock_flac, mock_convert, mock_remove_cover_image, mock_listdir, mock_get_metadata):
        """Test handling of FLAC files with missing metadata."""
        mock_flac.return_value = MagicMock(spec=FLAC)
        mock_flac.return_value.pictures = []
        mock_flac.return_value.get.return_value = [None]  # Simulate missing metadata

        processor = FileProcessor('E:\\1. IPOD LIBRARY\\256 AAC', FLACToAACConversion())
        processor.create_directory_structure = MagicMock(return_value='target_dir')
        processor.process_files()

        # Conversion should be attempted, even with missing metadata, but filename should be handled correctly
        mock_convert.assert_called_once_with('missing_metadata_file.flac', 'target_dir\\00. Unknown Title.m4a')
        mock_remove_cover_image.assert_called_once()
        mock_listdir.assert_called_once()


if __name__ == '__main__':
    unittest.main()
