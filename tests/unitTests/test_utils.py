# file_processor/tests/test_utils.py

import unittest
from unittest.mock import patch, MagicMock
from utils import FileUtils
from mutagen.flac import FLAC



class TestFileUtils(unittest.TestCase):
    @patch('utils.re.match')
    def test_is_windows_directory_format(self, mock_match):
        mock_match.return_value = True
        result = FileUtils.is_windows_directory_format('C:\\some\\path')
        self.assertTrue(result)
        mock_match.assert_called_once()

    @patch.object(FLAC, '__getitem__', return_value=['Michael Jackson'])
    def test_get_metadata(self, mock_getitem):
        audio = FLAC('C:\\Users\\ferra\\Desktop\\SMILE\\02 - They Don’t Care About Us.flac')
        result = FileUtils.get_metadata(audio, 'artist')
        print(result)
        self.assertEqual(result, 'Michael Jackson')
        # mock_getitem.assert_called_once_with('artist')

    @patch('utils.FLAC')
    def test_remove_cover_image(self, MockFLAC):
        mock_audio = MockFLAC.return_value
        mock_audio.pictures = [MagicMock()]
        FileUtils.remove_cover_image('file.flac')
        mock_audio.clear_pictures.assert_called_once()
        mock_audio.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
