from abc import ABC, abstractmethod
from datetime import datetime

from typeguard import typechecked


class MoveMapBase(ABC):
    @typechecked
    @abstractmethod
    def get_dst_path(self, date: datetime.date) -> dict:
        '''Returns ready destination path by received date'''
