from abc import ABC, abstractmethod

from src.types import FileWay, MoveReport

from libs import Either


class MoverBase(ABC):

    @abstractmethod
    def move(self,
             file_way: FileWay,
             move_mode: bool) -> MoveReport:
        ''''''

    @abstractmethod
    def set_dst_folder(self, value: str) -> Either:
        '''
        Raise an exception if the target folder is incorrect
        '''

    @abstractmethod
    def create_and_set_dst_folder(self, value: str) -> None:
        ''''''
