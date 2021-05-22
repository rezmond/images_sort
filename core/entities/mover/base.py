from abc import ABC, abstractmethod

from core.types import FileWay

from libs import Either


class MoverBase(ABC):

    @abstractmethod
    def move(self,
             file_way: FileWay,
             move_mode: bool) -> None:
        '''Moves files'''

    @property
    @abstractmethod
    def on_move_finished(self):
        '''Calls when the moving has finished.'''

    @on_move_finished.setter
    def on_move_finished(self, val):
        '''
        It was created for the "+=" operator could work with that property
        '''

    @abstractmethod
    def set_dst_folder(self, value: str) -> Either:
        '''
        Raise an exception if the target folder is incorrect
        '''

    @abstractmethod
    def create_and_set_dst_folder(self, value: str) -> None:
        ''''''
