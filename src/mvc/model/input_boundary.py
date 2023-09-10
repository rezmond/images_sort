from abc import ABC, abstractmethod

from typeguard import typechecked


class InputBoundary(ABC):

    @typechecked
    @abstractmethod
    def clean_mode(self, enable: bool) -> None:
        '''Set clean mode'''

    @typechecked
    @abstractmethod
    def scan_mode(self, enable: bool) -> None:
        '''Set scan mode'''

    @typechecked
    @abstractmethod
    def move_mode(self, enable: bool) -> None:
        '''Set move mode'''

    @typechecked
    @abstractmethod
    def set_dst_folder(self, value: str) -> None:
        ''''''

    @typechecked
    @abstractmethod
    def set_src_folder(self, value: str) -> None:
        ''''''
