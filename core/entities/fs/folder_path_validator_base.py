from abc import ABC, abstractmethod

from typeguard import typechecked


class FolderPathValidatorBase(ABC):

    @typechecked
    @abstractmethod
    def validate(self, param_value: str, param_humanize: str) -> None:
        '''Validate the folder by path'''
