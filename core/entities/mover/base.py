# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from core.types import ScanResult
from core.utils import MoveResult


class MoverBase(metaclass=ABCMeta):

    @abstractmethod
    def move(self,
             scanned: ScanResult,
             dst_folder: str,
             move_mode: bool) -> MoveResult:
        '''Moves files'''

    @property
    @abstractmethod
    def on_image_moved(self):
        '''Calls when an image have moved.'''

    @on_image_moved.setter
    def on_image_moved(self, val):
        '''
        It was created for the "+=" operator could work with that property
        '''

    @property
    @abstractmethod
    def on_move_finished(self):
        '''Calls when the moving has finished.'''

    @on_move_finished.setter
    def on_move_finished(self, val):
        '''
        It was created for the "+=" operator could work with that property
        '''
