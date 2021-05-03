from abc import ABC, abstractmethod

from typeguard import typechecked

from core.types import ScanReport


class OutputBoundary(ABC):

    @typechecked
    @abstractmethod
    def scanned_file(self, path: str, total: int) -> None:
        '''Outputs the metainfo about found file'''

    @typechecked
    @abstractmethod
    def scan_finished(self, scan_report: ScanReport) -> None:
        '''Show scan report'''
