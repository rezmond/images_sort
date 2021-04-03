from abc import ABCMeta, abstractstaticmethod


class FsManipulatorBase(metaclass=ABCMeta):

    @abstractstaticmethod
    def move(self, src: str, dst: str) -> None:
        '''Moves a fs node'''

    @abstractstaticmethod
    def copy(self, src: str, dst: str) -> None:
        '''Copies a fs node'''

    @abstractstaticmethod
    def delete(self, path: str) -> None:
        '''Deletes a fs node'''

    @abstractstaticmethod
    def makedirs(self, path: str) -> None:
        '''Makes dirs by provided path'''
