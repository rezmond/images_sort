from typeguard import typechecked

from core.entities.scanner import ScannerBase
from core.entities.mover import MoverBase
from core.types import ScanReport, MoveType, MoveReport
from libs import Either, Right
from .output_boundary import OutputBoundary
from .input_boundary import InputBoundary


class MoverModel(InputBoundary):

    @typechecked
    def __init__(
        self,
        mover: MoverBase,
        scanner: ScannerBase,
    ):
        self._mover = mover
        self._scanner = scanner
        self._output_boundary = None
        self._file_ways = []
        self._src_folder = None
        self._dst_folder = None
        self._modes = {
            'clean': False,
            'move': False,
            'scan': False,
            'verbosity': 0,
        }

    @typechecked
    def set_output_boundary(self, output_boundary: OutputBoundary):
        self._output_boundary = output_boundary

    @typechecked
    def clean_mode(self, enable: bool):
        self._modes['clean'] = enable

    @typechecked
    def scan_mode(self, enable: bool):
        self._modes['scan'] = enable

    @typechecked
    def move_mode(self, enable: bool):
        self._modes['move'] = enable

    @typechecked
    def scan(self) -> None:
        for file_way in self._scanner.scan(self._src_folder):
            self._file_ways.append(file_way)
            self._output_boundary.scanned_file(
                file_way.src, len(self._file_ways))

        self._output_boundary.scan_finished(self._get_scan_report())

        if self._modes['scan']:
            self._output_boundary.finish()
        else:
            self._move_if_confirmed()

    @typechecked
    def _get_scan_report(self) -> ScanReport:
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

    @typechecked
    def _move_if_confirmed(self) -> None:
        if self._modes['move']:
            self.move()
            return

        scan_report = self._get_scan_report()
        movable_count = len(scan_report.movable)
        is_confirmed = self._output_boundary.confirm(
            f'Do You want to move the {movable_count} files')

        if not is_confirmed:
            self._output_boundary.finish()

    @typechecked
    def move(self) -> None:
        self._mover\
            .set_dst_folder(self._dst_folder)\
            .either(
                self._resolve_dst_does_not_exist,
                lambda _: Right(None),
            ).map(lambda _: self._move())

    @typechecked
    def _move(self) -> None:
        def _move_generator():
            for file_way in self._file_ways:
                yield self._mover.move(file_way, self._modes['clean'])

        self._output_boundary.on_move_started(
            _move_generator(), length=len(self._file_ways))

    @typechecked
    def _resolve_dst_does_not_exist(self, dst: str) -> Either:
        return self._output_boundary\
            .request_create_dst_folder(dst)\
            .map(self._mover.create_and_set_dst_folder)

    @InputBoundary.on_move_finished.getter
    def on_move_finished(self):
        return self._mover.on_move_finished

    def set_dst_folder(self, value: str) -> None:
        self._dst_folder = value

    def set_src_folder(self, value: str) -> None:
        self._src_folder = value
