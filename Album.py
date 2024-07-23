import os
from typing import Dict, Any
from utils import FileUtils
import logging

logger = logging.getLogger(__name__)

class Album:
    def __init__(self):
        self.songs = []
        self.folder = self.input_directory()
        self.metadata = dict()

    @staticmethod
    def input_directory() -> str:
        """Prompt user for input directory and validate it."""
        directory = input("Please enter the source directory for the album you want to work with\n")
        while not os.path.isdir(directory) or not FileUtils.is_windows_directory_format(directory):
            logger.warning(f"Invalid directory entered: {directory}")
            directory = input("PLEASE ENTER A VALID DIRECTORY\n")
        print(f'You selected the album directory: {directory}\n')
        logger.info(f"Selected album directory: {directory}")
        return directory

    def add_song(self, song: 'Song'):
        self.songs.append(song)

    def find_metadata(self):
        self.metadata = self.songs[0].get_metadata()
        if not self.metadata or any('error' in meta_detail for meta_detail in self.metadata):
            logger.warning("No FLAC files found or metadata extraction failed for all files.")
            print("Metadata not found, please enter the metadata manually\n")
            self.metadata['artist'] = input("Artist: \n")
            self.metadata['album'] = input("Album Title: \n")
            self.metadata['date'] = input("Date: \n")
        logger.info(f"Metadata set from first file: Artist: {self.metadata['artist']}, Album: {self.metadata['album'] }, "
                    f"Date: {self.metadata['date'] }")
        return self.metadata
