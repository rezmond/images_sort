
from abc import ABCMeta, abstractstaticmethod


class FolderCheckerBase(metaclass=ABCMeta):
    @abstractstaticmethod
    def isfolder(path: str) -> None:
        '''Return true if the pathname refers to an existing directory'''
