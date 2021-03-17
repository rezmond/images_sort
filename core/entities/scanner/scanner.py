# -*- coding: utf-8 -*-

import os
from datetime import datetime
from typing import Tuple, List, Union
from dateutil.parser import isoparse

from typeguard import typechecked
import exifread

from utils import full_path
from core.types import ScanResult
from core.utils import InverseOfControlContainer
from ..utils import validate_folder_path
from ..move_map import MoveMap
from .base import ScannerBase

MAX_TIME_STRING_LENGTH = 19


def get_exif_data(path: str) -> Union[exifread.classes.IfdTag, None]:
    with open(path, 'rb') as current_file:
        tags = exifread.process_file(current_file)
    exif_data = tags.get('EXIF DateTimeOriginal', None)
    return exif_data


class Scanner(ScannerBase):

    ALLOWED_EXTENSIONS = (
        '.jpg',
        '.JPG',
        '.jpeg',
        '.png'
    )

    @typechecked
    def __init__(self, ioc: InverseOfControlContainer) -> None:
        self._scanned = None
        self._ioc = ioc
        self._scanning_observable = ioc.get('observable')()

    @property
    def on_file_found(self):
        return self._scanning_observable

    @on_file_found.setter
    def on_file_found(self, value):
        '''
        It was created for the "+=" operator could work with that property
        '''

    @staticmethod
    def _get_datetime(src):
        try:
            return isoparse(src)
        except ValueError:
            cropped = src[:MAX_TIME_STRING_LENGTH]
            return datetime.strptime(cropped, '%Y:%m:%d %H:%M:%S')

    @typechecked
    def _get_images_list(
            self, current_dir_path: str) -> Tuple[List[dict], List[str]]:
        """
        It returns all suitable by extension files taking into account nesting.
        Plus the path list of not images.
        """

        images = []
        not_images = []
        for node_name in os.listdir(current_dir_path):
            node_path = os.path.join(current_dir_path, node_name)
            if not os.path.isfile(node_path):
                sub_scanner = type(self)(self._ioc)
                sub_scanner.on_file_found += self._scanning_observable.update
                sub_images, sub_not_images = sub_scanner\
                    ._get_images_list(node_path)
                images.extend(sub_images)
                not_images.extend(sub_not_images)
                continue

            self._scanning_observable.update(node_path)

            if self._is_allowed_extension(node_path):
                images.append({
                    'path': full_path(node_path),
                    'name': node_name
                })
                continue

            not_images.append(node_path)
        return images, not_images

    def _is_allowed_extension(self, node_path):
        """
        Is the file name extension allowed
        """
        return os.path.splitext(node_path)[1] in self.ALLOWED_EXTENSIONS

    @typechecked
    def scan(
        self, src_folder_path: str
    ) -> None:
        self._validate_src(src_folder_path)
        # формирование структуры по exif
        no_exif = []
        move_map = MoveMap()
        img_files_info, not_img_file_path = self\
            ._get_images_list(src_folder_path)

        sorted_files_info = sorted(
            img_files_info, key=lambda x: x['name'], reverse=True)

        for file_dict in sorted_files_info:
            exif_data = get_exif_data(file_dict['path'])

            if not exif_data:
                no_exif.append(file_dict['path'])
                continue

            date = self._get_datetime(exif_data.values)
            move_map.add_data(date, file_dict)

        data = move_map.get_map()
        print("data", data)
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
