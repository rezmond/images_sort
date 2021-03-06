# -*- coding: utf-8 -*-

from .mover import Mover
from ..utils import MoveResult


class MoverModel:

    def __init__(self):
        self._mover = Mover()
        self._src_folder = None
        self._dst_folder = None

    def move(self) -> MoveResult:
        move_result = self._mover.move(self._src_folder, self._dst_folder)
        return move_result

    @property
    def on_image_moved(self):
        return self._mover.on_image_moved

    @on_image_moved.setter
    def on_image_moved(self, value):
        '''
        It was created for the "+=" operator could work with that property
        '''

    @property
    def on_move_finished(self):
        return self._mover.on_move_finished

    @on_move_finished.setter
    def on_move_finished(self, value):
        '''
        It was created for the "+=" operator could work with that property
        '''

    def set_dst_folder(self, value: str) -> None:
        self._dst_folder = value

    def set_src_folder(self, value: str) -> None:
        self._src_folder = value
