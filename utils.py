import re
import logging
import requests
from typing import Optional
import os
from mutagen.flac import FLAC
from Album import Album

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
    def sanitize_directory_name(name: str) -> str:
        """Sanitize directory names to remove invalid characters."""
        return re.sub(r'[<>:"/|?*]', '', name)

    @staticmethod
    def extract_year(date):
        # Regular expression to match the date format YYYY-MM-DD
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'

        # Check if the input matches the date pattern
        if re.match(date_pattern, date):
            # If it matches, extract the year
            return date.split('-')[0]
        else:
            # If it doesn't match, return the input as the year (assuming it's already a year)
            return date

    @staticmethod
    def longest_common_suffix(titles):
        # Reverse each title to treat suffix as prefix, making it easier to compare
        reversed_titles = [title[::-1] for title in titles]
        common_reversed_suffix = ""
        for chars in zip(*reversed_titles):
            if len(set(chars)) == 1:
                common_reversed_suffix += chars[0]  # Add common character
            else:
                break  # Stop when characters differ
        return common_reversed_suffix[::-1]  # Reverse back to get the original suffix

    @staticmethod
    def get_metadata(audio: FLAC, key: str, default: str = 'Unknown') -> str:
        """Retrieve metadata from audio, case-insensitively."""
        key_lower = key.lower()
        audio_dict = {k.lower(): v for k, v in audio.items()}

        try:
            value = audio_dict[key_lower][0]  # Use dictionary-style access to get the correct metadata value
        except KeyError:
            value = default
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
            logger.error(f"Error removing cover image from {file_path} : {e}")

    # Sample function to clean the album name
    @staticmethod
    def clean_album_name(album_name: str) -> str:
        # Remove text within parentheses
        album_name = re.sub(r'\s*\(.*?\)\s*', '', album_name)
        # Remove text within square brackets
        album_name = re.sub(r'\s*\[.*?]\s*', '', album_name)
        # Remove any leading or trailing whitespace
        return album_name.strip()

    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize the given filename by removing or replacing characters not allowed in Windows file systems.

        Args:
        filename (str): The original filename or folder name.

        Returns:
        str: The sanitized filename or folder name.
        """
        # Define a regex pattern for illegal characters
        illegal_chars = r'[\\/:*?"<>|]'

        # Replace illegal characters with underscores
        sanitized = re.sub(illegal_chars, '_', filename)

        return sanitized

    @staticmethod
    def save_album_cover(target_dir: str, album: Album, image_data: bytes) -> str:
        artist_with_hyphens = album.metadata['artist'].replace(" ", "-").lower()
        album_title_with_hyphens = album.metadata['album'].replace(" ", "-").lower()
        cover_image_path = os.path.join(target_dir, f"cover-{artist_with_hyphens}-{album_title_with_hyphens}.jpg")

        # Save the cover image to a file
        with open(cover_image_path, 'wb') as file:
            file.write(image_data)

        # Return the path to the cover image
        return cover_image_path

    @staticmethod
    def fetch_album_cover(target_dir: str, album: Album) -> Optional[str]:
        """Fetch album cover image from iTunes API."""
        base_url = "https://itunes.apple.com"
        album_title = album.metadata['album']
        artist_name = album.metadata['artist']

        # Step 1: Find the artist
        search_artist_url = f"{base_url}/search"
        params = {
            'term': artist_name,
            'entity': 'musicArtist',
            'attribute': 'artistTerm',
            'limit': 10,
            'media': 'music'
        }
        response = requests.get(search_artist_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['resultCount'] > 0:
                artist_id = None
                for result in data.get('results', []):
                    if result['artistName'].lower() == artist_name.lower():
                        artist_id = result['artistId']
                        break

                if not artist_id:
                    return None
                # Step 2: Search for the album by artist ID
                lookup_album_url = f"{base_url}/lookup"
                params = {
                    'id': artist_id,
                    'entity': 'album',
                    'media': 'music'
                }
                response = requests.get(lookup_album_url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    # Filter albums by name
                    for result_album in data.get('results'):
                        if 'collectionName' in result_album:
                            collection = result_album['collectionName']
                            if album_title.lower() in collection.lower() or collection.lower() in album_title.lower():
                                artwork_url = result_album.get('artworkUrl100')  # URL for 100x100 image

                                if not artwork_url:
                                    print(f"No artwork URL found for album: {album_title} by artist: {artist_name}")
                                    return None

                                # Construct URL for higher resolution artwork
                                artwork_url = artwork_url.replace('100x100bb', '1000x1000bb')

                                # Download the cover image
                                cover_response = requests.get(artwork_url)
                                cover_response.raise_for_status()

                                return FileUtils.save_album_cover(target_dir, album, cover_response.content)
        else:
            return None
