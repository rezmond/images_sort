from typing import Tuple

from typeguard import typechecked

from .base import ControllerBase


class ConsoleViewController(ControllerBase):
    def __init__(self, *args, **kwars):
        super(ConsoleViewController, self).__init__(*args, **kwars)

    def show(self):
        self._view.show()

    @typechecked
    def enable_moved_images_log(self, enable: bool = True):
        if enable:
            self._model.on_move_finished += self._handle_move_finished

    @typechecked
    def _handle_move_finished(self, move_pair: Tuple[str, str]) -> None:
        self._view.handle_move_finished(move_pair)
