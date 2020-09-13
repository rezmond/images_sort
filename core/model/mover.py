# -*- coding: utf-8 -*-

import os
import shutil

import filecmp

from .scanner import Scanner, YearType
from ..utils import MoveResult, Observable


class Mover:

    def __init__(self):
        self._move_result = None
        self._moved_image_event_listeners = Observable()
        self._move_finish_event_listeners = Observable()

    @staticmethod
    def _cmp_files(dst_dir, file_dict):
        """
        Check the destination folder for already existed files with the
        same names.

        If a file exists and it is identical, then the current method
        will return fully path to target folder with the "already_exists"
        result type.

        If a file with that name exists but it is not identical, then the 
        current method will rename the target file name added a number til
        the name will unique.

        :return: (<result_type>, <fully/path/to/file>)
        :rtype: typle(str, str)
        """
        num = 1
        curr_file_name = os.path.split(file_dict['path'])[1]
        dst_file_path = os.path.join(dst_dir, curr_file_name)

        if not os.path.isfile(dst_file_path):
            return 'moved', dst_file_path

        base_file_name, extension = os.path.splitext(curr_file_name)

        while os.path.isfile(dst_file_path):
            if filecmp.cmp(file_dict['path'], dst_file_path):
                return 'already_exists', dst_file_path

            curr_file_name = '{}_{}{}'.format(
                base_file_name, num, extension)
            dst_file_path = os.path.join(dst_dir, curr_file_name)
            num += 1
        return 'moved', dst_file_path

    @staticmethod
    def __make_dir_if_not_exists(path):
        """Если целевой папки не было создано"""
        if not os.path.exists(path):
            os.makedirs(path)

    def move(self, src_folder: str, dst_folder: str) -> MoveResult:
        self._validate_src_dst(src_folder, dst_folder)

        scanner = Scanner()
        move_map, no_exif, not_images = scanner.scan(src_folder)
        self._move_result = MoveResult([], [], no_exif, not_images)

        # перемещение файлов
        year_items = move_map.items()
        for y_name, y_value in year_items:
            month_items = y_value.items()
            self._move_by_month(dst_folder, y_name, month_items)

        self._move_finish_event_listeners.update(self._move_result)
        return self._move_result

    def _move_by_month(
        self,
        dst_folder: str,
        year_name: str,
        month_items: YearType,
    ):
        for m_name, m_value in month_items:
            dst_dir_path = (
                os.path.join(dst_folder, year_name, m_name))

            self.__make_dir_if_not_exists(dst_dir_path)

            for file_dict in m_value:
                result_type, result_path = (
                    self._cmp_files(dst_dir_path, file_dict))

                if result_type == 'moved':
                    shutil.copy2(file_dict['path'], result_path)
                    self._moved_image_event_listeners.update(
                        (file_dict['path'], result_path))

                getattr(self._move_result, result_type)\
                    .append(file_dict['path'])

    @property
    def on_image_moved(self):
        return self._moved_image_event_listeners

    @on_image_moved.setter
    def on_image_moved(self, value):
        pass

    @property
    def on_move_finished(self):
        return self._move_finish_event_listeners

    @on_move_finished.setter
    def on_move_finished(self, value):
        '''
        It was created for the "+=" operator could work with that property
        '''

    def _validate_src_dst(self, src: str, dst: str) -> None:
        '''
        Without typechecked because it will check arguments manually
        '''
        params_check_list = (
            (src, 'source'),
            (dst, 'destination'),
        )
        for param_value, param_humanize in params_check_list:
            if not param_value:
                raise ValueError(
                    'The {0} folder\'s path did not set.'
                    ' Please set the {0} folder path and try again.'
                    .format(param_humanize))

            if not os.path.isabs(param_value):
                raise ValueError(
                    'The {} folder path should be absolute, but got "{}"'
                    .format(param_humanize, param_value))
