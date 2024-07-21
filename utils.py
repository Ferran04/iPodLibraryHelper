import os
import re
import logging
from mutagen.flac import FLAC

logger = logging.getLogger(__name__)


class FileUtils:
    @staticmethod
    def is_windows_directory_format(path: str) -> bool:
        """Check if the given path is in Windows directory format."""
        # Regular expression for matching a Windows directory path
        logger.debug(f"Checking if directory path is in Windows format: {path}")
        pattern = r'^[a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\?)*$'
        result = re.match(pattern, path) is not None
        logger.debug(f"Directory format check result: {result}")
        return result

    @staticmethod
    def get_metadata(audio: FLAC, key: str, default: str = 'Unknown') -> str:
        """Retrieve metadata from audio."""
        value = audio.get(key, [default])[0]
        logger.debug(f"Retrieved metadata for key '{key}': {value}")
        return value

    @staticmethod
    def remove_cover_image(file_path: str) -> None:
        """Remove cover image from a FLAC file if present."""
        logger.info(f"Removing cover image from file: {file_path}")
        try:
            audio = FLAC(file_path)
            if audio.pictures:
                audio.clear_pictures()
                audio.save()
                logger.debug(f"Removed cover image from {file_path}")
            else:
                logger.debug(f"No cover image found in {file_path}")
        except Exception as e:
            logger.error(f"Error removing cover image from {file_path}")

