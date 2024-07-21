# file_processor/tests/test_utils.py

import unittest
from unittest.mock import patch, MagicMock
from utils import FileUtils
from mutagen.flac import FLAC


class TestFileUtils(unittest.TestCase):
    @patch('file_processor.utils.re.match')
    def test_is_windows_directory_format(self, mock_match):
        mock_match.return_value = True
        result = FileUtils.is_windows_directory_format('C:\\some\\path')
        self.assertTrue(result)
        mock_match.assert_called_once()

    @patch.object(FLAC, 'get', return_value=['Artist'])
    def test_get_metadata(self, mock_get):
        audio = FLAC('file.flac')
        result = FileUtils.get_metadata(audio, 'artist')
        self.assertEqual(result, 'Artist')
        mock_get.assert_called_once_with('artist')

    @patch('file_processor.utils.FLAC')
    def test_remove_cover_image(self, MockFLAC):
        mock_audio = MockFLAC.return_value
        mock_audio.pictures = [MagicMock()]
        FileUtils.remove_cover_image('file.flac')
        mock_audio.clear_pictures.assert_called_once()
        mock_audio.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
