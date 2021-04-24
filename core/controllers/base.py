from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from typeguard import typechecked

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
        self._model = model
        self._view = view_class(self, self._model)

    @abstractmethod
    @typechecked
    def clean_mode(self, enable: bool) -> None:
        '''Enables the clean_mode of the model'''

    @abstractmethod
    @typechecked
    def enable_moved_images_log(self, enable: bool = True):
        '''Sabscribes to notifications from the model about moved media'''

    def set_dst_folder(self, *args):
        self._model.set_dst_folder(*args)

    def set_src_folder(self, *args):
        self._model.set_src_folder(*args)

    def move(self):
        self._model.move()
