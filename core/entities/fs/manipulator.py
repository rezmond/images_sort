from abc import abstractstaticmethod

from .folder_checker_base import FolderCheckerBase


class FsManipulatorBase(FolderCheckerBase):

    @abstractstaticmethod
    def move(src: str, dst: str) -> None:
        '''Moves a fs node'''

    @abstractstaticmethod
    def copy(src: str, dst: str) -> None:
        '''Copies a fs node'''

    @abstractstaticmethod
    def delete(path: str) -> None:
        '''Deletes a fs node'''

    @abstractstaticmethod
    def makedirs(path: str) -> None:
        '''Makes dirs by provided path'''

    @abstractstaticmethod
    def isfile(path: str) -> None:
        '''Test whether a path is a regular file'''
