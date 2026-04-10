from abc import ABCMeta, abstractmethod


class FolderCheckerBase(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def isfolder(path: str) -> bool:
        """Return true if the pathname refers to an existing directory"""
