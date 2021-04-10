from abc import ABC, abstractmethod

from core.types import FileWay


class MoverBase(ABC):

    @abstractmethod
    def move(self,
             file_way: FileWay,
             dst_folder: str,
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
