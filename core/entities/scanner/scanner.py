from typing import Tuple, Iterator

from typeguard import typechecked

from core.types import MoveType, FileWay
from ..fs import FolderExtractorBase, FolderPathValidator, FolderCheckerBase
from ..exceptions import FolderNotFoundError
from .base import ScannerBase
from .date_extractor_base import DateExtractorBase
from .move_map_base import MoveMapBase


class Scanner(ScannerBase):

    @typechecked
    def __init__(
            self,
            date_extractor: DateExtractorBase,
            folder_extractor: FolderExtractorBase,
            fs_manipulator: FolderCheckerBase,
            move_map: MoveMapBase,
    ) -> None:
        self._date_extractor = date_extractor
        self._folder_extractor = folder_extractor
        self._folder_path_validator = FolderPathValidator(fs_manipulator)
        self._move_map = move_map

    @typechecked
    def _get_media_pairs(self, dir_path: str) -> Iterator[Tuple[str, bool]]:
        pathes = self._folder_extractor.folder_to_file_pathes(dir_path)
        for path in pathes:
            if self._date_extractor.is_allowed_extension(path):
                yield path, True
                continue

            yield path, False

    @typechecked
    def scan(self, src_folder: str) -> Iterator[FileWay]:
        self._validate_src(src_folder)

        for path, is_media in self._get_media_pairs(src_folder):
            if not is_media:
                yield FileWay(type=MoveType.NO_MEDIA, src=path)
                continue

            date = self._date_extractor.get_date(path)

            if not date:
                yield FileWay(type=MoveType.NO_DATA, src=path)
                continue

            yield FileWay(
                type=MoveType.MEDIA,
                src=path,
                dst=self._move_map.get_dst_path(date),
            )

    def _validate_src(self, path):
        either_existed = self._folder_path_validator.validate('source', path)

        if either_existed.is_left():
            raise FolderNotFoundError('source', path)
