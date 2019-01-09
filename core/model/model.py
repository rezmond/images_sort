# -*- coding: utf-8 -*-

from .mover import Mover
from ..utils import MoveResult


class Model:

    def __init__(self):
        self._mover = Mover()

    def move(self, src_folder: str, dst_folder: str) -> MoveResult:
        move_result = self._mover.move(src_folder, dst_folder)
        return move_result

    @property
    def on_image_moved(self):
        return self._mover.on_image_moved

    @on_image_moved.setter
    def on_image_moved(self, value):
        pass
