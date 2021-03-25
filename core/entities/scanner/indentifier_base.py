# -*- coding: utf-8 -*-

import os
from abc import ABCMeta, abstractclassmethod
from datetime import datetime


class IdentifierBase(metaclass=ABCMeta):
    ALLOWED_EXTENSIONS = tuple()

    def is_allowed_extension(self, node_path: str) -> bool:
        """
        Is the file name extension allowed
        """
        return os.path.splitext(node_path)[1] in self.ALLOWED_EXTENSIONS

    @abstractclassmethod
    def get_date(cls, path: str) -> datetime.date:
        '''Returns a date based on entity'''
