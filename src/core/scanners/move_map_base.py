from abc import ABC, abstractmethod
from datetime import datetime

from typeguard import typechecked


class MoveMapBase(ABC):
    @typechecked
    @abstractmethod
    def get_dst_path(self, date: datetime) -> str:
        """Returns ready destination path by received date"""
