from abc import ABCMeta, abstractmethod
from typing import Iterable

from typeguard import typechecked

"""
TODO: Get rid of that in favor of FsManipulation ?
"""


class FolderExtractorBase(metaclass=ABCMeta):
    @staticmethod
    @typechecked
    @abstractmethod
    def folder_to_file_pathes(path: str) -> Iterable[str]:
        """
        Returns the iterable within file path
        """
