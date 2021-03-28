from abc import ABCMeta, abstractstaticmethod
from typing import Iterable, Tuple

from typeguard import typechecked


class FolderExtractorBase(metaclass=ABCMeta):

    @abstractstaticmethod
    @typechecked
    def folder_to_file_pathes(path: str) -> Iterable[Tuple[str, str]]:
        '''
        Returns the iterable within file path with names
        built by accepted path to a folder
        '''
