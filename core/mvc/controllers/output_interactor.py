from abc import ABC, abstractmethod
from typing import Iterable, Optional

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
    def show_moving_progress(
        self, moved_reports: Iterable[MoveReport], length: int,
        should_report_be_shown: bool
    ) -> None:
        ''''''

    @typechecked
    def show_total_move_report(
            self,
            report: TotalMoveReport,
            log_to_file: Optional[str]) -> None:
        ''''''
