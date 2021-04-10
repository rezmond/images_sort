from abc import ABC, abstractmethod
from typing import Iterator

from core.types import FileWay


class ScannerBase(ABC):

    @abstractmethod
    def scan(self, src_folder_path: str) -> Iterator[FileWay]:
        '''Yields the object that describes possible way for moving a file'''
