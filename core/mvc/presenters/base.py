from abc import ABC, abstractmethod

from typeguard import typechecked

from core.types import ScanReport
from ..model import OutputBoundary
from .output_interactor import OutputInteractor


class PresenterBase(OutputBoundary, ABC):

    @typechecked
    def __init__(self, output_interactor: OutputInteractor) -> None:
        self._output_interactor = output_interactor

    @typechecked
    def scanned_file(self, path: str, total: int) -> None:
        self._output_interactor.scanned_file(path, total)

    @typechecked
    def scan_finished(self, scan_report: ScanReport) -> None:
        self._output_interactor.show_scan_report(scan_report)

    @typechecked
    def finish(self) -> None:
        self._output_interactor.close()

    @typechecked
    @abstractmethod
    def show(self) -> None:
        '''Shows user interface'''
