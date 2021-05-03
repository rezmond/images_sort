from abc import ABC, abstractmethod

from typeguard import typechecked


class InputInteractor(ABC):

    @typechecked
    @abstractmethod
    def show(self) -> None:
        '''Show a view'''
