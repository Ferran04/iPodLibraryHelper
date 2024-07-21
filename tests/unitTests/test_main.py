# file_processor/tests/test_main.py

import unittest
from unittest.mock import patch, MagicMock
from main import get_conversion_strategy, get_directory_path
from converters import FLACToAACConversion, FLACToWAVConversion


class TestMain(unittest.TestCase):
    @patch('file_processor.main.input', return_value='1')
    def test_get_conversion_strategy(self, mock_input):
        strategy = get_conversion_strategy()
        self.assertIsInstance(strategy, FLACToAACConversion)

    @patch('file_processor.main.get_conversion_strategy', return_value=FLACToAACConversion())
    def test_get_directory_path(self, mock_get_conversion_strategy):
        dir_path = get_directory_path(FLACToAACConversion())
        self.assertEqual(dir_path, 'E:\\1. IPOD LIBRARY\\256 AAC')


if __name__ == '__main__':
    unittest.main()
