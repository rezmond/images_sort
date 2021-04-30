from abc import ABCMeta, abstractmethod

from ..model import MoverModel
from ..controllers.base import ControllerBase


class ViewBase(metaclass=ABCMeta):

    view_class = None

    def __init__(
        self,
        controller: ControllerBase,
        model: MoverModel,
    ):
        self._controller = controller
        self._model = model

    @abstractmethod
    def show(self):
        '''Shows the app view'''
