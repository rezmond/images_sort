from abc import ABC, abstractmethod

from typing import Iterable
from typeguard import typechecked

from core.types import ScanReport, MoveReport
from libs import Either


class OutputBoundary(ABC):

    @typechecked
    @abstractmethod
    def scanned_file(self, path: str, total: int) -> None:
        '''Outputs the metainfo about found file'''

    @typechecked
    @abstractmethod
    def scan_finished(self, scan_report: ScanReport) -> None:
        '''Show scan report'''

    @typechecked
    @abstractmethod
    def finish(self) -> None:
        '''Finish a stage'''

    @typechecked
    @abstractmethod
    def confirm(self, message: str) -> bool:
        '''Show message and return confirmation'''

    @typechecked
    @abstractmethod
    def request_create_dst_folder(self, dst: str) -> Either:
        '''
        Resolve the case when user-provided destination path is not a folder
        '''

    @typechecked
    @abstractmethod
    def on_move_started(self, moved_reports: Iterable[MoveReport]) -> None:
        ''''''
