import os
import shutil

from typeguard import typechecked
from typing import Iterable, Tuple

from core.entities import FsManipulatorBase, FolderExtractorBase


class FsManipulator(FsManipulatorBase, FolderExtractorBase):
    move = shutil.move
    copy = shutil.copy2
    delete = os.remove
    makedirs = os.makedirs

    @staticmethod
    @typechecked
    def folder_to_file_pathes(path: str) -> Iterable[Tuple[str, str]]:
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                yield filename, os.path.join(dirpath, filename)
