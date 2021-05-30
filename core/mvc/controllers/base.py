from abc import ABC, abstractmethod

from typeguard import typechecked

from core.types import ScanReport, MoveReport
from ..model import InputBoundary, OutputBoundary
from .io_interactor import IoInteractor


class ControllerBase(OutputBoundary, ABC):

    @typechecked
    def __init__(
            self,
            input_boundary: InputBoundary,
    ) -> None:
        self._input_boundary = input_boundary
        self._io_interactor = None

    @typechecked
    def set_io_interactor(self, io_interactor: IoInteractor) -> None:
        self._io_interactor = io_interactor

    @typechecked
    def clean_mode(self, enable: bool) -> None:
        self._input_boundary.clean_mode(enable)

    @typechecked
    def scan_mode(self, enable: bool) -> None:
        self._input_boundary.scan_mode(enable)

    @typechecked
    def move_mode(self, enable: bool) -> None:
        self._input_boundary.move_mode(enable)

    def set_dst_folder(self, *args):
        self._input_boundary.set_dst_folder(*args)

    def set_src_folder(self, *args):
        self._input_boundary.set_src_folder(*args)

    def scan(self):
        return self._input_boundary.scan()

    @typechecked
    def scanned_file(self, path: str, total: int) -> None:
        self._io_interactor.scanned_file(path, total)

    @typechecked
    def scan_finished(self, scan_report: ScanReport) -> None:
        self._io_interactor.show_scan_report(scan_report)

    @typechecked
    def finish(self) -> None:
        self._io_interactor.close()

    @typechecked
    @abstractmethod
    def show(self) -> None:
        '''Shows user interface'''
