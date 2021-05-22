import os

from typeguard import typechecked

from libs import Right, Left, Either
from ..exceptions import (
    NoArgumentPassedError,
    RelativeFolderPathError,
)
from .folder_checker_base import FolderCheckerBase


class FolderPathValidator:

    @typechecked
    def __init__(self, fs_manipulator: FolderCheckerBase) -> None:
        self._fs_manipulator = fs_manipulator

    @typechecked
    def validate(self, name: str, path: str) -> Either:

        if not path:
            raise NoArgumentPassedError(name)

        if not os.path.isabs(path):
            raise RelativeFolderPathError(name, path)

        if not self._fs_manipulator.isfolder(path):
            return Left(path)

        return Right(path)
