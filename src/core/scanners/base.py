from abc import ABC, abstractmethod
from typing import Iterator

from src.types import FileWay


class ScannerBase(ABC):
    @abstractmethod
    def scan(self, folder: str) -> Iterator[FileWay]:
        """Yields the object that describes the nature of moving candidate in terms of media files collection"""


class TargetFolderScannerBase(ABC):
    @abstractmethod
    def scan(self, folder: str) -> None:
        """Scans the folder and store the results in an inner map"""

    @abstractmethod
    def detect_duplicates(self, src_file: str) -> bool:
        """
        Check if a source file conflicts with any existing file in target folder.
        Returns True if conflict exists (i.e., file should not replace the existed one, but it should be moved with a new name).

        Main goal: Add all media files to the database without losing any file.
        If no conflict is detected, we can move or copy the file.
        In case of an error checking the file size (uncertainty), return True to create a duplicate with a new name.
        This ensures that no media file is lost.

        Args:
            src_file (str): Source file path

        Returns:
            bool: True if conflict detected OR if we cannot determine (error case), False otherwise
        """

