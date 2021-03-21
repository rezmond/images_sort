from typeguard import typechecked

from core.types import Comparator
from .manipulator import FsManipulatorBase


class FsActions:
    @typechecked
    def __init__(
        self,
        fs_manipulator: FsManipulatorBase,
        comparator: Comparator,
        move_mode: bool,
        delete_mode: bool,
    ):
        self._mover = fs_manipulator.move\
            if move_mode else fs_manipulator.copy

        self._remover = fs_manipulator.delete\
            if delete_mode else self._delete_stub

        self._comparator = comparator

    @staticmethod
    @typechecked
    def _delete_stub(path: str):
        '''Do nothing'''

    @typechecked
    def move(self, src: str, dst: str) -> None:
        self._mover(src, dst)

    @typechecked
    def delete(self, path: str) -> None:
        self._remover(path)

    @typechecked
    def compare(self, src: str, dst: str) -> bool:
        return self._comparator(src, dst)
