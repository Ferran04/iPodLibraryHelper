# file_processor/converters.py

import subprocess
import logging
from abc import ABC, abstractmethod

# Configure logging
logger = logging.getLogger(__name__)


class ConversionStrategy(ABC):
    @abstractmethod
    def convert(self, source_file: str, target_file_base: str) -> None:
        """Convert the source file to the target file format."""
        pass


# Concrete implementation of the abstract base class
class FLACToAACConversion(ConversionStrategy):
    def convert(self, source_file: str, target_file_base: str) -> None:
        """Convert FLAC file to AAC format."""
        target_file = f"{target_file_base}.m4a"
        print(f"Converting {source_file} to {target_file} using AAC conversion.")
        logger.info(f"Converting {source_file} to {target_file}")
        command = [
            'ffmpeg', '-i', source_file,
            '-c:a', 'aac', '-b:a', '256k',
            '-aac_pns', '0', '-ar', '44100',
            target_file
        ]
        try:
            subprocess.run(command, check=True)
            logger.info(f"Conversion successful: {source_file} -> {target_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Conversion error for {source_file}: {e}")
            print(f"Error converting {source_file}: e")


class FLACToWAVConversion(ConversionStrategy):
    def convert(self, source_file: str, target_file_base: str) -> None:
        """Convert FLAC file to WAV format."""
        target_file = f"{target_file_base}.wav"
        command = [
            'ffmpeg', '-i', source_file,
            target_file
        ]
        try:
            subprocess.run(command, check=True)
            logger.info(f"Conversion successful: {source_file} -> {target_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Conversion error for {source_file}: {e}")
            print(f"Error converting {source_file}: e")


class Converter:
    def __init__(self, strategy: ConversionStrategy):
        self.strategy = strategy

    def convert(self, source_file: str, target_file: str) -> None:
        self.strategy.convert(source_file, target_file)
