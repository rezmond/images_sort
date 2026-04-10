from abc import ABCMeta, abstractmethod
from typing import Iterable

from typeguard import typechecked



class FolderExtractorBase(metaclass=ABCMeta):
    @staticmethod
    @typechecked
    @abstractmethod
    def folder_to_file_pathes(path: str) -> Iterable[str]:
        """
        Returns the iterable within file path
        """
