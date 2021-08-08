from datetime import datetime
from abc import ABCMeta, abstractmethod


class DateExtractorBase(metaclass=ABCMeta):

    @abstractmethod
    def is_allowed_extension(self, path: str) -> bool:
        '''Determines, can the instance work with passed extension'''

    @abstractmethod
    def get_date(self, path: str) -> datetime.date:
        '''
        Returns the data by the passed path to the media file if they
        are extractable.
        '''
