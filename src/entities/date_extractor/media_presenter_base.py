import os
from abc import ABCMeta, abstractmethod
from datetime import datetime
from operator import itemgetter

from utils import pipe


class MediaPresenterBase(metaclass=ABCMeta):
    ALLOWED_EXTENSIONS = tuple()

    @classmethod
    def get_extensions(cls):
        return cls.ALLOWED_EXTENSIONS

    @abstractmethod
    def get_date(self, path: str) -> datetime.date:
        '''Returns a date based on media'''

    @staticmethod
    def _get_clean_file_name(path):
        return pipe(
            os.path.split,
            itemgetter(1),
            os.path.splitext,
            itemgetter(0),
        )(path)
