from abc import ABC, abstractmethod

from typeguard import typechecked


class InputInteractor(ABC):
    pass

    # @abstractmethod
    # @typechecked
    # def enable_moved_images_log(self, enable: bool = True):
    #     '''Sabscribes to notifications from the model about moved media'''
