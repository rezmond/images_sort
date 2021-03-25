# -*- coding: utf-8 -*-

import os
from typing import Tuple, List

from typeguard import typechecked

from utils import full_path
from core.types import ScanResult, FileDescriptor
from core.utils.base import Observable
from ..utils import validate_folder_path
from ..move_map import MoveMap
from .base import ScannerBase
from .indentifier_base import IdentifierBase

ImagesSeparated = Tuple[List[FileDescriptor], List[str]]


class Scanner(ScannerBase):

    @typechecked
    def __init__(self, observable: Observable, identifier: IdentifierBase) -> None:
        self._scanned = None
        self._scanning_observable = observable
        self._identifier = identifier

    @property
    def on_file_found(self):
        return self._scanning_observable

    @on_file_found.setter
    def on_file_found(self, value):
        '''
        It was created for the "+=" operator could work with that property
        '''

    def subscanner(self):
        '''It is a stub for future overriding by ioc'''
        return self

    @typechecked
    def _scan_folder(self, node_path: str) -> ImagesSeparated:
        scanner = self.subscanner()
        scanner.on_file_found += self._scanning_observable.update
        return scanner._get_images_list(node_path)

    @typechecked
    def _get_images_list(self, current_dir_path: str) -> ImagesSeparated:
        """
        It returns all suitable by extension files taking into account nesting.
        Plus the path list of not images.
        """

        images = []
        not_images = []
        for node_name in os.listdir(current_dir_path):
            node_path = os.path.join(current_dir_path, node_name)
            if not os.path.isfile(node_path):
                sub_images, sub_not_images = self._scan_folder(node_path)
                images.extend(sub_images)
                not_images.extend(sub_not_images)
                continue

            self._scanning_observable.update(node_path)

            if self._identifier.is_allowed_extension(node_path):
                file_descriptor = FileDescriptor(
                    full_path(node_path),
                    node_name
                )
                images.append(file_descriptor)
                continue

            not_images.append(node_path)
        return images, not_images

    @typechecked
    def scan(
        self, src_folder_path: str
    ) -> None:
        self._validate_src(src_folder_path)

        no_exif = []
        move_map = MoveMap()
        img_files_info, not_img_file_path = self\
            ._get_images_list(src_folder_path)

        sorted_files_info = sorted(
            img_files_info, key=lambda x: x.name, reverse=True)

        for file_descriptor in sorted_files_info:
            date = self._identifier.get_date(file_descriptor.path)

            if not date:
                no_exif.append(file_descriptor.path)
                continue

            move_map.add_data(date, file_descriptor)

        self._scanned = ScanResult(
            move_map.get_map(),
            no_exif,
            not_img_file_path,
        )

    @typechecked
    def get_data(self) -> ScanResult:
        return self._scanned

    def _validate_src(self, source_folder):
        validate_folder_path(source_folder, 'source')
