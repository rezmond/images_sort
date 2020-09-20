# -*- coding: utf-8 -*-

from typing import Tuple

from typeguard import typechecked

from ..views import ConsoleView
from .base import ControllerBase


class ConsoleViewController(ControllerBase):
    view_class = ConsoleView

    def __init__(self, *args):
        super(ConsoleViewController, self).__init__(*args)
        self._view.show()

    def clean_mode(self, *args):
        self._model.clean_mode(*args)

    @typechecked
    def enable_moved_images_log(self, enable: bool = True):
        if enable:
            self._model.on_image_moved += self._handle_image_moved

    @typechecked
    def _handle_image_moved(self, move_pair: Tuple[str, str]) -> None:
        self._view.handle_image_moved(move_pair)
