from abc import ABC, abstractmethod
from typing import Iterator

from src.types import FileWay


class ScannerBase(ABC):
    @abstractmethod
    def scan(self, folder: str) -> Iterator[FileWay]:
        """Yields the object that describes the nature of moving candidate in terms of media files collection"""

