# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from datetime import datetime


class IdentifierBase(metaclass=ABCMeta):
    ALLOWED_EXTENSIONS = tuple()

    def __init__(self):
        self._checkers = []

    def is_allowed_extension(self, node_path: str) -> bool:
        """
        Is the file name extension allowed
        """
        return any((
            checker.is_allowed_extension(node_path)
            for checker in self._checkers
        ))

    @abstractmethod
    def get_date(self, path: str) -> datetime.date:
        '''Returns a date based on entity'''
