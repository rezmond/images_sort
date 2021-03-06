# -*- coding: utf-8 -*-

import os
from datetime import datetime
from typing import Dict, Tuple, List

from typeguard import typechecked
import exifread

from ...utils import full_path

BlocksType = List[Dict[str, str]]
YearType = Dict[str, BlocksType]
MoveMap = Dict[str, YearType]


class Scanner:

    ALLOWED_EXTENSIONS = (
        '.jpg',
        '.JPG',
        '.jpeg',
        '.png'
    )

    BLOCKS = {
        'winter (begin)': (1, 2),
        'spring': (3, 5),
        'summer': (6, 8),
        'autumn': (9, 11),
        'winter (end)': (12, 12),
    }

    def _get_block_name(self, month):
        """
        Return month name in human readable format
        :param month: month number(from 1 to 12)
        :rtype: str
        """
        assert month in range(1, 13), \
            'Month number must be from 1 to 12. Not "{0}"'.format(month)

        for key, value in self.BLOCKS.items():
            if value[0] <= month <= value[1]:
                return key

    @staticmethod
    def _get_datetime(src):
        return datetime.strptime(src, '%Y:%m:%d %H:%M:%S')

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
                sub_images, sub_not_images = self._get_images_list(node_path)
                images.extend(sub_images)
                not_images.extend(sub_not_images)
                continue

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
    ) -> Tuple[MoveMap, List[str], List[str]]:
        self._validate_source_folder(src_folder_path)
        # формирование структуры по exif
        no_exif = []
        move_map = {}
        img_files_info, not_img_file_path = self\
            ._get_images_list(src_folder_path)

        for file_dict in img_files_info:
            with open(file_dict['path'], 'rb') as current_file:
                tags = exifread.process_file(current_file)
            exif_data = tags.get('EXIF DateTimeOriginal', None)
            if not exif_data:
                no_exif.append(file_dict['path'])
                continue
            date = self._get_datetime(exif_data.values)
            # years
            year_in_string = str(date.year)
            if year_in_string not in set(move_map.keys()):
                move_map[year_in_string] = {}
            # month
            month_in_string = self._get_block_name(date.month)
            if month_in_string not in set(move_map[year_in_string].keys()):
                move_map[year_in_string][month_in_string] = []
            move_map[year_in_string][month_in_string]\
                .append(file_dict)

        return move_map, no_exif, not_img_file_path

    def _validate_source_folder(self, source_folder):

        if not os.path.isabs(source_folder):
            raise ValueError(
                f'The source folder path should be absolute, but got'
                ' "{source_folder}"'
            )

        if not os.path.isdir(source_folder):
            raise ValueError(
                f'The folder "{source_folder}" not found')
