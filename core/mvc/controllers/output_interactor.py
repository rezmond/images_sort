from abc import ABC, abstractmethod
from typing import ContextManager, Iterable

from typeguard import typechecked

from core.types import ScanReport, MoveReport
from libs import Either


class OutputInteractor(ABC):

    @typechecked
    @abstractmethod
    def scanned_file(self, path: str, total: int) -> None:
        '''Outputs the metainfo about found file'''

    @typechecked
    @abstractmethod
    def show(self) -> None:
        '''Show a view'''

    @typechecked
    @abstractmethod
    def show_scan_report(self, scan_report: ScanReport) -> None:
        ''''''

    @typechecked
    @abstractmethod
    def request_create_dst_folder(self, dst: str) -> Either:
        ''''''

    @typechecked
    @abstractmethod
    def file_moved_report_to_str(self, report: MoveReport) -> str:
        ''''''

    @typechecked
    @abstractmethod
    def move_context(
        self, moved_reports: Iterable[MoveReport]
    ) -> ContextManager[Iterable[MoveReport]]:
        ''''''
