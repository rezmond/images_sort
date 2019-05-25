# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from ..model import MoverModel
from ..controllers.base import ControllerBase
from ..utils import MoveResult


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

    @abstractmethod
    def _show_move_report(self, move_result: MoveResult) -> None:
        '''Shows the result of the moving'''
