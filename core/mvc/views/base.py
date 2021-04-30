from abc import ABCMeta, abstractmethod

from ..controllers.base import ControllerBase


class ViewBase(metaclass=ABCMeta):

    view_class = None

    def __init__(
        self,
        controller: ControllerBase,
    ):
        self._controller = controller

    @abstractmethod
    def show(self):
        '''Shows the app view'''
