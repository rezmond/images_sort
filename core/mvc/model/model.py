from typeguard import typechecked

from core.entities.scanner import ScannerBase
from core.entities.mover import MoverBase

from .output_boundary import OutputBoundary


class MoverModel:

    @typechecked
    def __init__(
        self,
        mover: MoverBase,
        scanner: ScannerBase,
        output_boundary: OutputBoundary
    ):
        self._mover = mover
        self._scanner = scanner
        self._output_boundary = output_boundary
        self._file_ways = []
        self._src_folder = None
        self._dst_folder = None
        self._clean_mode = False
        self._scan_mode = False

    @typechecked
    def clean_mode(self, enable: bool):
        self._clean_mode = enable

    @typechecked
    def scan_mode(self, enable: bool):
        self._scan_mode = enable

    def scan(self):
        for file_way in self._scanner.scan(self._src_folder):
            self._file_ways.append(file_way)
            self._output_boundary.scanned_file(
                file_way.src, len(self._file_ways))

    def move(self) -> None:
        '''
            TODO: separate to two phases:
                1. Scan
                2. (If confirmed) Move
        '''
        for file_way in self._file_ways:
            self._mover.move(file_way, self._dst_folder, self._clean_mode)

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
