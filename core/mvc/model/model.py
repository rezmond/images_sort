from typeguard import typechecked

from core.entities.scanner import ScannerBase
from core.entities.mover import MoverBase
from core.types import ScanReport, MoveType

from .output_boundary import OutputBoundary
from .input_boundary import InputBoundary


class MoverModel(InputBoundary):

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
        self._modes = {
            'clean': False,
            'move': False,
            'scan': False,
        }

    @typechecked
    def clean_mode(self, enable: bool):
        self._modes['clean'] = enable

    @typechecked
    def scan_mode(self, enable: bool):
        self._modes['scan'] = enable

    @typechecked
    def move_mode(self, enable: bool):
        self._modes['move'] = enable

    def scan(self):
        for file_way in self._scanner.scan(self._src_folder):
            self._file_ways.append(file_way)
            self._output_boundary.scanned_file(
                file_way.src, len(self._file_ways))

        self._output_boundary.scan_finished(self._get_scan_report())

        if self._modes['scan']:
            self._output_boundary.finish()

    def _get_scan_report(self):
        report = ScanReport()
        for file_way in self._file_ways:
            if file_way.type == MoveType.MEDIA:
                report.movable.append(file_way)
            elif file_way.type == MoveType.NO_MEDIA:
                report.no_media.append(file_way)
            elif file_way.type == MoveType.NO_DATA:
                report.no_data.append(file_way)
            else:
                raise Exception(f'Incorrect file way type "{file_way.type}"')
        return report

    def move(self) -> None:
        '''
            TODO: separate to two phases:
                1. Scan
                2. (If confirmed) Move
        '''
        for file_way in self._file_ways:
            self._mover.move(file_way, self._dst_folder, self._modes['clean'])

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
