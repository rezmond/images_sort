from abc import ABC, abstractmethod

from typeguard import typechecked


class OutputBoundary(ABC):

    @typechecked
    @abstractmethod
    def scanned_file(self, path: str, total: int) -> None:
        '''Outputs the metainfo about found file'''
