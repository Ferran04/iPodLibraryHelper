import os
from typing import Dict, Any, List
from tqdm import tqdm
from mutagen.flac import FLAC
import logging

from utils import FileUtils
from converters import Converter, ConversionStrategy

logger = logging.getLogger(__name__)


class FileProcessor:
    def __init__(self, library_directory: str, strategy: ConversionStrategy):
        self.dir_library = library_directory
        self.converter = Converter(strategy)

    @staticmethod
    def extract_flac_metadata(file_path: str) -> Dict[str, Any]:
        """Extract metadata from a FLAC file."""
        logger.info(f"Extracting metadata from file: {file_path}")
        metadata = {}
        try:
            audio = FLAC(file_path)
            metadata['file'] = file_path
            metadata['title'] = FileUtils.get_metadata(audio, 'title')
            metadata['album'] = FileUtils.get_metadata(audio, 'album')
            metadata['artist'] = FileUtils.get_metadata(audio, 'artist')
            metadata['date'] = FileUtils.get_metadata(audio, 'date')
            metadata['track_number'] = FileUtils.get_metadata(audio, 'track_number')
        except Exception as e:
            logger.error(f"Metadata extraction error for {file_path}: {e}")
            metadata['error'] = str(e)
        return metadata

    def create_directory_structure(self, artist: str, album: str, date: str) -> str:
        """Create directory structure based on metadata."""
        album_dir = f"{album} ({date})"
        target_dir = os.path.join(self.dir_library, artist, album_dir)
        os.makedirs(target_dir, exist_ok=True)
        logger.info(f"Created directory: {target_dir}")
        return target_dir

    def get_flac_files_info(self, directory: str) -> List[Dict[str, Any]]:
        """Retrieve and process metadata for all FLAC files in the directory."""
        flac_metadata_list = []
        for filename in os.listdir(directory):
            if filename.lower().endswith('.flac'):
                file_path = os.path.join(directory, filename)
                FileUtils.remove_cover_image(file_path)
                metadata = self.extract_flac_metadata(file_path)
                flac_metadata_list.append(metadata)
        return flac_metadata_list

    def input_directory(self) -> str:
        """Prompt user for input directory and validate it."""
        directory = input("Please enter the source directory you want to work with\n")
        while not os.path.isdir(directory) or not FileUtils.is_windows_directory_format(directory):
            logger.warning(f"Invalid directory entered: {directory}")
            directory = input("PLEASE ENTER A VALID DIRECTORY\n")
        print(f'You selected the directory {directory}\n')
        logger.info(f"Selected directory: {directory}")
        return directory

    def process_files(self) -> None:
        """Process FLAC files in the given directory."""
        logger.info("Starting file processing")
        directory = self.input_directory()
        flac_metadata_list = self.get_flac_files_info(directory)

        if not flac_metadata_list or any('error' in metadata for metadata in flac_metadata_list):
            # If any metadata entry is not valid, we ask for manual intervention
            logger.warning("No FLAC files found or metadata extraction failed for all files.")
            print("Metadata not found, please enter the metadata manually\n")
            artist = input("Artist: \n")
            album = input("Album Title: \n")
            date = input("Date: \n")
        else:
            # All metadata entries are valid at this point
            first_metadata = flac_metadata_list[0]
            artist = first_metadata.get('artist', 'Unknown Artist')
            album = first_metadata.get('album', 'Unknown Album')
            date = first_metadata.get('date', 'Unknown Date')
            logger.info(f"Metadata set from first file: Artist: {artist}, Album: {album}, Date: {date}")

        target_dir = self.create_directory_structure(artist, album, date)
        print(f"Files will be processed into: {target_dir}")

        for metadata in tqdm(flac_metadata_list, desc="Processing files", unit="file"):
            if 'error' in metadata:
                logger.error(f"Error processing {metadata['file']}: {metadata['error']}")
                print("Error processing {}: {}".format(metadata['file'], metadata['error']))
                continue

            title = metadata.get('title', 'Unknown Title')
            track_number = metadata.get('track_number', '00').zfill(2)

            target_base_file_name = f"{track_number}. {title}"
            target_base_file_path = os.path.join(target_dir, target_base_file_name)

            self.converter.convert(metadata['file'], target_base_file_path)
            logger.info(f"Removing original FLAC file: {metadata['file']}")
            os.remove(metadata['file'])

        print("Processing completed.")
        logger.info("Processing completed.")


