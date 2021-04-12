from typing import Callable, Tuple, Iterator

from typeguard import typechecked

from core.types import MoveType, FileWay
from core.utils.base import Observable
from ..fs import FolderExtractorBase
from .base import ScannerBase
from .date_extractor_base import DateExtractorBase
from .move_map_base import MoveMapBase


class Scanner(ScannerBase):

    @typechecked
    def __init__(
            self,
            observable: Observable,
            date_extractor: DateExtractorBase,
            folder_extractor: FolderExtractorBase,
            validate_folder_path: Callable[[str, str], None],
            move_map: MoveMapBase,
    ) -> None:
        self._scanning_observable = observable
        self._date_extractor = date_extractor
        self._folder_extractor = folder_extractor
        self._validate_folder_path = validate_folder_path
        self._move_map = move_map

    @property
    def on_file_found(self):
        return self._scanning_observable

    @on_file_found.setter
    def on_file_found(self, value):
        '''
        It was created for the "+=" operator could work with that property
        '''

    @typechecked
    def _get_media_pairs(self, dir_path: str) -> Iterator[Tuple[str, bool]]:
        pathes = self._folder_extractor.folder_to_file_pathes(dir_path)
        for path in pathes:
            self._scanning_observable.update(path)

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

    def _validate_src(self, source_folder):
        self._validate_folder_path(source_folder, 'source')
