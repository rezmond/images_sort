from abc import ABC, abstractmethod

from libs import Either
from src.types import FileWay, MoveReport


class MoverBase(ABC):
    @abstractmethod
    def move(self, file_way: FileWay, move_mode: bool) -> MoveReport:
        """"""

    @abstractmethod
    def set_dst_folder(self, dst: str) -> Either[str, str]:
        """
        Returns Either monad with the dst path. Left in case of the target is not a folder.

        Raise an exception if the target folder is incorrect
        """

    @abstractmethod
    def create_and_set_dst_folder(self, dst: str) -> None:
        """"""
