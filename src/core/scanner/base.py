from abc import ABC, abstractmethod
from typing import Iterator

from src.types import FileWay


class ScannerBase(ABC):

    @abstractmethod
    def scan(self, src_folder: str) -> Iterator[FileWay]:
        '''Yields the object that describes possible way for moving a file'''
