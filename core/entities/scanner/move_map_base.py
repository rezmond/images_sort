from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from typeguard import typechecked


class MoveMapBase(ABC):
    @typechecked
    @abstractmethod
    def add_data(self, date: datetime.date, data: Any) -> None:
        '''Adds the date to map'''

    @typechecked
    @abstractmethod
    def get_map(self) -> dict:
        '''Returns ready data as dict'''
