# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractstaticmethod

from .types import ScanResult

class ScannerBase(metaclass=ABCMeta):

    @abstractmethod
    def scan(
        self, src_folder_path: str
    ) -> None:
        pass

    @abstractstaticmethod
    def get_data() -> ScanResult:
        pass
