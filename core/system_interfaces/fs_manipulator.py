import os
import shutil

from typeguard import typechecked
from typing import Iterable

from core.entities import FsManipulatorBase, FolderExtractorBase


class FsManipulator(FsManipulatorBase, FolderExtractorBase):
    @staticmethod
    def move(src: str, dst: str) -> None:
        shutil.move(src, dst)

    @staticmethod
    def copy(src: str, dst: str) -> None:
        shutil.copy2(src, dst)

    @staticmethod
    def delete(path: str) -> None:
        os.remove(path)

    @staticmethod
    def makedirs(path: str) -> None:
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def isfile(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def isfolder(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    @typechecked
    def folder_to_file_pathes(path: str) -> Iterable[str]:
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                yield os.path.join(dirpath, filename)
