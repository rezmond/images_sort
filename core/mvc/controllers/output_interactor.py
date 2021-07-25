from abc import ABC, abstractmethod
from typing import ContextManager, Iterable, Optional

from typeguard import typechecked

from core.types import ScanReport, MoveReport, TotalMoveReport
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
    def move_in_context(
        self, moved_reports: Iterable[MoveReport], length: int,
        should_report_be_shown: bool
    ) -> ContextManager[Iterable[MoveReport]]:
        ''''''

    @typechecked
    def show_total_move_report(
            self,
            report: TotalMoveReport,
            log_to_file: Optional[str]) -> None:
        ''''''
