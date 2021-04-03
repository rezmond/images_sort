from typing import Callable, Tuple, List

from typeguard import typechecked

from core.types import ScanResult, FileDescriptor
from core.utils.base import Observable
from ..fs import FolderExtractorBase
from ..move_map import MoveMap
from .base import ScannerBase
from .date_extractor_base import DateExtractorBase

ImagesSeparated = Tuple[List[FileDescriptor], List[str]]


class Scanner(ScannerBase):

    @typechecked
    def __init__(
            self,
            observable: Observable,
            date_extractor: DateExtractorBase,
            folder_extractor: FolderExtractorBase,
            validate_folder_path: Callable[[str, str], None],
    ) -> None:
        self._scanned = None
        self._scanning_observable = observable
        self._date_extractor = date_extractor
        self._folder_extractor = folder_extractor
        self._validate_folder_path = validate_folder_path

    @property
    def on_file_found(self):
        return self._scanning_observable

    @on_file_found.setter
    def on_file_found(self, value):
        '''
        It was created for the "+=" operator could work with that property
        '''

    @typechecked
    def _get_images_list(self, current_dir_path: str) -> ImagesSeparated:
        """
        It returns all suitable by extension files taking into account nesting.
        Plus the path list of not medias.
        """

        medias = []
        not_media = []
        files_with_names = self._folder_extractor\
            .folder_to_file_pathes(current_dir_path)
        for node_name, node_path in files_with_names:
            self._scanning_observable.update(node_path)

            if self._date_extractor.is_allowed_extension(node_path):
                medias.append(FileDescriptor(node_path, node_name))
                continue

            not_media.append(node_path)

        return medias, not_media

    @typechecked
    def scan(self, src_folder_path: str) -> None:
        self._validate_src(src_folder_path)

        no_data = []
        move_map = MoveMap()
        img_files_info, not_img_file_path = self\
            ._get_images_list(src_folder_path)

        sorted_files_info = sorted(
            img_files_info, key=lambda x: x.name, reverse=True)

        for file_descriptor in sorted_files_info:
            date = self._date_extractor.get_date(file_descriptor.path)

            if not date:
                no_data.append(file_descriptor.path)
                continue

            move_map.add_data(date, file_descriptor)

        self._scanned = ScanResult(
            move_map.get_map(),
            no_data,
            not_img_file_path,
        )

    @typechecked
    def get_data(self) -> ScanResult:
        return self._scanned

    def _validate_src(self, source_folder):
        self._validate_folder_path(source_folder, 'source')
