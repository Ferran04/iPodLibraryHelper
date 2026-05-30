import os
from typing import Dict, Any
from tqdm import tqdm
from mutagen.flac import FLAC
import logging
from typing import Optional

from utils import FileUtils
from converters import Converter, ConversionStrategy
from Album import Album
from Song import Song
from Folder import Folder
logger = logging.getLogger(__name__)


class FileProcessor:
    def __init__(self, library_directory: str, strategy: ConversionStrategy):
        self.dir_library = library_directory
        self.converter = Converter(strategy)
        destructive = input(
            "Will you want to delete the files after the process? type 1 if yes, otherwise type any other thing\n")
        if destructive == '1':
            self.destructive = True
        else:
            self.destructive = False

    @staticmethod
    def extract_cover_from_file(file_path: str) -> Optional[bytes]:
        """Extract metadata from a FLAC file."""
        logger.info(f"Extracting cover image from file: {file_path}")
        cover = None
        try:
            audio = FLAC(file_path)
            # Check if there's at least one picture
            if audio.pictures:
                if audio.pictures[0]:
                    cover = audio.pictures[0].data  # Extract the first picture
                else:
                    logger.info(f"cover image not present in the file {file_path}")

        except Exception as e:
            logger.error(f"cover image extraction error for {file_path}: {e}")
        return cover

    @staticmethod
    def extract_flac_metadata(file_path: str) -> Dict[str, Any]:
        """Extract metadata from a FLAC file."""
        logger.info(f"Extracting metadata from file: {file_path}")
        metadata = {}
        try:
            audio = FLAC(file_path)
            metadata['file'] = file_path
            metadata['title'] = FileUtils.get_metadata(audio, 'title')
            metadata['album'] = FileUtils.clean_album_name(FileUtils.get_metadata(audio, 'album'))
            metadata['artist'] = FileUtils.get_metadata(audio, 'artist')
            if metadata['artist'] != 'Unknown':
                audio['albumartist'] = metadata['artist']
            else:
                metadata['album_artist'] = FileUtils.get_metadata(audio, 'albumartist')
                if metadata['album_artist'] != 'Unknown':
                    metadata['artist'] = metadata['album_artist']
                else:
                    raise Exception("Couldn't find the artist")
            metadata['year'] = FileUtils.extract_year(FileUtils.get_metadata(audio, 'date'))
            metadata['track_number'] = FileUtils.get_metadata(audio, 'tracknumber')
            disc_number = FileUtils.get_metadata(audio, 'discnumber')
            metadata['disc_number'] = disc_number if disc_number else 1
        except Exception as e:
            logger.error(f"Metadata extraction error for {file_path}: {e}")
            metadata['error'] = str(e)
        return metadata

    def create_directory_structure(self, artist: str, album: str, date: str) -> str:
        """Create directory structure based on metadata."""
        album_dir = FileUtils.sanitize_directory_name(f"{artist.upper()}\\{album.upper()}")
        target_dir = os.path.join(self.dir_library, album_dir)
        os.makedirs(target_dir, exist_ok=True)
        logger.info(f"Created directory: {target_dir}")
        print(f"Files will be processed into: {target_dir}")

        return target_dir

    def get_flac_files_info(self, album: Album):
        """Retrieve and process metadata for all FLAC files in the directory."""
        count_files = 0
        song_titles = []
        for filename in os.listdir(album.folder):
            if filename.lower().endswith('.flac'):
                file_path = os.path.join(album.folder, filename)
                FileUtils.remove_cover_image(file_path)
                metadata = self.extract_flac_metadata(file_path)
                song_titles.append(metadata['title'])
                album.add_song(Song(file_path, metadata, album))
                count_files += 1

        if len(song_titles) > 1:
            common_suffix = FileUtils.longest_common_suffix(song_titles)
            if common_suffix:
                album.remove_suffixes(common_suffix)
                for filename in os.listdir(album.folder):
                    if filename.lower().endswith('.flac'):
                        file_path = os.path.join(album.folder, filename)
                        audio = FLAC(file_path)
                        audio['title'] = [Album.clean_title(audio['title'][0], common_suffix)]
                        audio['comment'] = common_suffix
                        audio.save()
        return count_files

    @staticmethod
    def find_cover_image(album_folder: str) -> Optional[str]:
        """Look for an image file named 'cover' on the album folder."""
        # List all files in the given album folder
        for file in os.listdir(album_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                return os.path.join(album_folder, file)
        return None

    # Define a separate method to handle cover selection
    def handle_cover_selection(self, target_dir, album):
        cover_path = self.find_cover_image(album.folder)
        if cover_path:
            choice = input("We found a cover in your folder. Do you want to use it or download one from the web? "
                           "1 (USE IT) 2 (USE WEB): ")
            if choice != '1':
                cover_path = FileUtils.fetch_album_cover(target_dir, album)
        else:
            cover_path = FileUtils.fetch_album_cover(target_dir, album)

        if cover_path is None:
            print("Could not find a cover image.")
            return None

        with open(cover_path, "rb") as file:
            image_bytes = file.read()
        FileUtils.save_album_cover(target_dir, album, image_bytes)

        return cover_path

    def process_files(self, current_folder: Folder) -> None:
        """Process FLAC files in the given directory."""
        logger.info("Starting file processing")

        folder_albums = current_folder.get_folder_albums()
        for album in folder_albums:
            if self.get_flac_files_info(album) == 0:
                continue
            album.find_metadata()
            target_dir = self.create_directory_structure(album.metadata['artist'], album.metadata['album'],
                                                         album.metadata['year'])

            cover = self.extract_cover_from_file(album.songs[0].file)
            # Fetch album cover
            if cover:
                print("Do you want to keep the same picture or not? 1 (KEEP) 2 (DO NOT KEEP)")
                choice = input("Enter your choice (1 or 2): ")

                if choice == '1':
                    cover_path = FileUtils.save_album_cover(target_dir, album, cover)
                else:
                    cover_path = self.handle_cover_selection(target_dir, album)
            else:
                cover_path = self.handle_cover_selection(target_dir, album)

            for song in tqdm(album.songs, desc="Processing files", unit="file"):
                metadata = song.metadata
                if 'error' in metadata:
                    logger.error(f"Error processing {metadata['file']}: {metadata['error']}")
                    print("Error processing {}: {}".format(metadata['file'], metadata['error']))
                    continue

                title = metadata.get('title', 'Unknown Title')
                track_number = metadata.get('track_number', '00').zfill(2)
                disc_number = metadata['disc_number']
                if disc_number is None or disc_number == 'Unknown':
                    target_base_file_name = f"{track_number}. {title}"
                else:
                    target_base_file_name = f"{disc_number}-{track_number}. {title}"
                target_base_file_path = os.path.join(target_dir, FileUtils.sanitize_filename(target_base_file_name))
                metadata['album_picture'] = cover_path
                self.converter.convert(metadata['file'], metadata['album_picture'], target_base_file_path)

                if self.destructive:
                    logger.info(f"Removing original FLAC file: {metadata['file']}")
                    os.remove(metadata['file'])

        print("Processing completed.")
        logger.info("Processing completed.")
