# -*- coding: utf-8 -*-

from abc import ABCMeta

from ..model import MoverModel


class ControllerBase(metaclass=ABCMeta):

    view_class = None

    def __init__(self, model: MoverModel):
        self._model = model
        self._view = self.view_class(self, self._model)

    def set_dst_folder(self, *args):
        self._model.set_dst_folder(*args)

    def set_src_folder(self, *args):
        self._model.set_src_folder(*args)
