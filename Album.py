import os
from typing import Dict, Any
import logging
import re
logger = logging.getLogger(__name__)

class Album:
    def __init__(self, album_folder: str):
        self.songs = []
        self.folder = album_folder
        self.metadata = dict()

    def add_song(self, song: 'Song'):
        self.songs.append(song)

    def find_metadata(self):
        self.metadata = self.songs[0].get_metadata()
        if not self.metadata or any('error' in meta_detail for meta_detail in self.metadata):
            logger.warning("No FLAC files found or metadata extraction failed for all files.")
            print("Metadata not found, please enter the metadata manually\n")
            self.metadata['artist'] = input("Artist: \n")
            self.metadata['album'] = input("Album Title: \n")
            self.metadata['year'] = input("Year: \n")
        logger.info(f"Metadata set from first file: Artist: {self.metadata['artist']}, Album: {self.metadata['album'] }, "
                    f"Year: {self.metadata['year'] }")
        return self.metadata

    @staticmethod
    def clean_title(title, common_suffix):
        # Use regex to remove the suffix only at the end
        return re.sub(re.escape(common_suffix) + r'$', '', title)

    def remove_suffixes(self, common_suffix):
        for song in self.songs:
            song.metadata['title'] = self.clean_title(song.metadata['title'], common_suffix)
