# -*- coding: utf-8 -*-

from typeguard import typechecked

from core.entities.scanner import ScannerBase
from core.entities.mover import MoverBase
from core.utils import MoveResult


class MoverModel:

    @typechecked
    def __init__(self, mover: MoverBase, scanner: ScannerBase):
        self._mover = mover
        self._scanner = scanner
        self._src_folder = None
        self._dst_folder = None
        self._clean_mode = False

    @typechecked
    def clean_mode(self, enable: bool):
        self._clean_mode = enable

    def move(self) -> MoveResult:
        self._scanner.scan(self._src_folder)
        scanned = self._scanner.get_data()
        move_result = self._mover.move(
            scanned, self._dst_folder, self._clean_mode)
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
    def on_file_found(self):
        return self._scanner.on_file_found

    @on_file_found.setter
    def on_file_found(self, value):
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
