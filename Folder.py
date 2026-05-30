import os
from typing import Dict, Any
from utils import FileUtils
import logging
from Album import Album

logger = logging.getLogger(__name__)


class Folder:
    def __init__(self, folder_name: str = ""):
        # self.album
        if folder_name == "":
            self.folder_name = self.input_directory()
        else:
            self.folder_name = folder_name
        pass

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

    def get_folder_albums(self):
        folder_albums = []
        count_folders = 0
        subfolders = [e for e in os.listdir(self.folder_name) if os.path.isdir(os.path.join(self.folder_name, e))]

        for folder in subfolders:
            folder_albums += Folder(os.path.join(self.folder_name, folder)).get_folder_albums()
            count_folders += 1

        if count_folders == 0:
            folder_albums.append(Album(self.folder_name))
        return folder_albums
