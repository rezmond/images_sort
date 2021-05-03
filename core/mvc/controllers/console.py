from typing import Tuple

from typeguard import typechecked

from .base import ControllerBase


class ConsoleViewController(ControllerBase):

    def show(self):
        self._input_interactor.show()

    @typechecked
    def enable_moved_images_log(self, enable: bool = True):
        if enable:
            self._input_boundary.on_move_finished += self._handle_move_finished

    @typechecked
    def _handle_move_finished(self, move_pair: Tuple[str, str]) -> None:
        self._input_interactor.handle_move_finished(move_pair)
