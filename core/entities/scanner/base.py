# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractstaticmethod

from core.types import ScanResult


class ScannerBase(metaclass=ABCMeta):

    @abstractmethod
    def scan(
        self, src_folder_path: str
    ) -> None:
        '''
            It creates the dictionary with output structure in an internal
            variable
        '''

    @abstractstaticmethod
    def get_data() -> ScanResult:
        '''It returns prepared the output structure'''
