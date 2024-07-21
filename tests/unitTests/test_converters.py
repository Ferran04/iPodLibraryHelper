# file_processor/tests/test_converters.py

import unittest
from unittest.mock import patch, MagicMock
from converters import FLACToAACConversion, FLACToWAVConversion, Converter


class TestFLACToAACConversion(unittest.TestCase):
    @patch('subprocess.run')
    def test_convert_flac_to_aac(self, mock_run):
        """
            Test the conversion from FLAC to AAC format.
            Verifies that the correct FFmpeg command is constructed and executed.
        """
        mock_run.return_value = None
        converter = FLACToAACConversion()
        converter.convert('source.flac', 'target')
        mock_run.assert_called_once_with([
            'ffmpeg', '-i', 'source.flac',
            '-c:a', 'aac', '-b:a', '256k',
            '-aac_pns', '0', '-ar', '44100',
            'target.m4a'
        ], check=True)


class TestFLACToWAVConversion(unittest.TestCase):
    @patch('subprocess.run')
    def test_convert_flac_to_wav(self, mock_run):
        """
            Test the conversion from FLAC to WAV format.
            Verifies that the correct FFmpeg command is constructed and executed.
        """
        mock_run.return_value = None
        converter = FLACToWAVConversion()
        converter.convert('source.flac', 'target')
        mock_run.assert_called_once_with([
            'ffmpeg', '-i', 'source.flac',
            'target.wav'
        ], check=True)


class TestConverter(unittest.TestCase):
    def test_convert_with_strategy(self):
        """
            Test that the Converter class uses the provided strategy correctly.
            Verifies that the strategy's convert method is called.
        """
        strategy = MagicMock()
        converter = Converter(strategy)
        converter.convert('source.flac', 'target')
        strategy.convert.assert_called_once_with('source.flac', 'target')


if __name__ == '__main__':
    unittest.main()
