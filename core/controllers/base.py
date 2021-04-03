from __future__ import annotations
from abc import ABCMeta
from typing import TYPE_CHECKING

from typeguard import check_type

from ..model import MoverModel

if TYPE_CHECKING:
    from ..views import ViewBase  # pragma: no cover


class ControllerBase(metaclass=ABCMeta):
    '''
    The "ViewBase" is circular dependecy.
    So it is tricky the type checking here
    '''

    def __init__(self, model: MoverModel, view_class: ViewBase):
        from ..views import ViewBase
        check_type('view_class', view_class, ViewBase)
        self._model = model
        self._view = view_class(self, self._model)

    def set_dst_folder(self, *args):
        self._model.set_dst_folder(*args)

    def set_src_folder(self, *args):
        self._model.set_src_folder(*args)

    def move(self):
        self._model.move()
