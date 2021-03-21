from abc import ABCMeta, abstractmethod


class FsManipulatorBase(metaclass=ABCMeta):

    @abstractmethod
    def move(self, src: str, dst: str) -> None:
        '''Moves a fs node'''

    @abstractmethod
    def copy(self, src: str, dst: str) -> None:
        '''Copies a fs node'''

    @abstractmethod
    def delete(self, path: str) -> None:
        '''Deletes a fs node'''

    @abstractmethod
    def makedirs(self, path: str) -> None:
        '''Makes dirs by provided path'''
