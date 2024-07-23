from typing import Dict, Any
from Album import Album


class Song:
    def __init__(self, file: str, metadata: Dict[str, Any], album: Album):
        self.album = album
        self.file = file
        self.metadata = metadata

    def get_metadata(self):
        return self.metadata
