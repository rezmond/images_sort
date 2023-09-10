from abc import ABCMeta, abstractstaticmethod
from typing import Iterable

from typeguard import typechecked


class FolderExtractorBase(metaclass=ABCMeta):

    @abstractstaticmethod
    @typechecked
    def folder_to_file_pathes(path: str) -> Iterable[str]:
        '''
        Returns the iterable within file path
        '''
