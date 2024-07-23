import os
from typing import Dict, Any, List
from tqdm import tqdm
from mutagen.flac import FLAC
import logging

from utils import FileUtils
from converters import Converter, ConversionStrategy
from Album import Album
from Song import Song

logger = logging.getLogger(__name__)


class FileProcessor:
    def __init__(self, library_directory: str, strategy: ConversionStrategy):
        self.dir_library = library_directory
        self.converter = Converter(strategy)
        while True:
            destructive = input("Will you want to delete the files after the process? type 1 if yes, otherwise type any other thing\n")
            if destructive is 1:
                self.destructive = True
                break
            else:
                self.destructive = False
                break
        self.destructive = destructive

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
            metadata['artist'] = FileUtils.get_metadata(audio, 'albumartist')
            metadata['date'] = FileUtils.get_metadata(audio, 'date')
            metadata['track_number'] = FileUtils.get_metadata(audio, 'tracknumber')
        except Exception as e:
            logger.error(f"Metadata extraction error for {file_path}: {e}")
            metadata['error'] = str(e)
        return metadata

    def create_directory_structure(self, artist: str, album: str, date: str) -> str:
        """Create directory structure based on metadata."""
        album_dir = FileUtils.sanitize_directory_name(f"{artist.upper()}\\{album} ({date})")
        target_dir = os.path.join(self.dir_library, album_dir)
        os.makedirs(target_dir, exist_ok=True)
        logger.info(f"Created directory: {target_dir}")
        print(f"Files will be processed into: {target_dir}")

        return target_dir

    def get_flac_files_info(self, album: Album):
        """Retrieve and process metadata for all FLAC files in the directory."""
        for filename in os.listdir(album.folder):
            if filename.lower().endswith('.flac'):
                file_path = os.path.join(album.folder, filename)
                FileUtils.remove_cover_image(file_path)
                metadata = self.extract_flac_metadata(file_path)
                album.add_song(Song(file_path, metadata, album))

    def process_files(self, album: Album) -> None:
        """Process FLAC files in the given directory."""
        logger.info("Starting file processing")
        self.get_flac_files_info(album)
        album.find_metadata()
        target_dir = self.create_directory_structure(album.metadata['artist'], album.metadata['album'],
                                                     album.metadata['date'])

        for song in tqdm(album.songs, desc="Processing files", unit="file"):
            metadata = song.metadata
            if 'error' in metadata:
                logger.error(f"Error processing {metadata['file']}: {metadata['error']}")
                print("Error processing {}: {}".format(metadata['file'], metadata['error']))
                continue

            title = metadata.get('title', 'Unknown Title')
            track_number = metadata.get('track_number', '00').zfill(2)

            target_base_file_name = f"{track_number}. {title}"
            target_base_file_path = os.path.join(target_dir, target_base_file_name)
            self.converter.convert(metadata['file'], target_base_file_path)

            if self.destructive:
                logger.info(f"Removing original FLAC file: {metadata['file']}")
                os.remove(metadata['file'])

        print("Processing completed.")
        logger.info("Processing completed.")
