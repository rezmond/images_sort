from abc import abstractmethod

from .folder_checker_base import FolderCheckerBase


class FsManipulatorBase(FolderCheckerBase):
    @staticmethod
    @abstractmethod
    def move(src: str, dst: str) -> None:
        """Moves a fs node"""

    @staticmethod
    @abstractmethod
    def copy(src: str, dst: str) -> None:
        """Copies a fs node"""

    @staticmethod
    @abstractmethod
    def delete(path: str) -> None:
        """Deletes a fs node"""

    @staticmethod
    @abstractmethod
    def makedirs(path: str) -> None:
        """Makes dirs by provided path"""

    @staticmethod
    @abstractmethod
    def isfile(path: str) -> bool:
        """Test whether a path is a regular file"""
