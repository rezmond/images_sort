# -*- coding: utf-8 -*-

import os
from typing import Callable

from typeguard import typechecked

from core.utils.base import Observable
from core.types import Comparator, ScanResult, YearType
from core.utils import MoveResult
from ..fs import FsManipulatorBase, FsActions
from ..utils import validate_folder_path
from .base import MoverBase


class Mover(MoverBase):

    @typechecked
    def __init__(
            self,
            observable_factory: Callable[[], Observable],
            fs_manipulator: FsManipulatorBase,
            comparator: Comparator
    ) -> None:
        self._fs_manipulator = fs_manipulator
        self._fs_actions = None
        self._comparator = comparator
        self._move_result = None
        self._move_function = None
        self._moved_image_event_listeners = observable_factory()
        self._move_finish_event_listeners = observable_factory()
        print("self._move_finish_event_listeners",
              self._move_finish_event_listeners)

    def _cmp_files(self, dst_dir, file_dict):
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
            if self._fs_actions.compare(file_dict['path'], dst_file_path):
                return 'already_exists', dst_file_path

            curr_file_name = '{}_{}{}'.format(
                base_file_name, num, extension)
            dst_file_path = os.path.join(dst_dir, curr_file_name)
            num += 1
        return 'moved', dst_file_path

    def __make_dir_if_not_exists(self, path):
        """Если целевой папки не было создано"""
        if not os.path.exists(path):
            self._fs_manipulator.makedirs(path)

    def move(self,
             scanned: ScanResult,
             dst_folder: str,
             move_mode: bool = False) -> MoveResult:
        self._validate_dst(dst_folder)
        self._fs_actions = FsActions(
            self._fs_manipulator, self._comparator, move_mode, move_mode)

        self._move_result = MoveResult(
            [], [], scanned.no_exif, scanned.not_images)

        # перемещение файлов
        year_items = scanned.move_map.items()
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
                    self._fs_actions.move(file_dict['path'], result_path)
                    self._moved_image_event_listeners.update(
                        (file_dict['path'], result_path))
                elif result_type == 'already_exists':
                    self._fs_actions.delete(file_dict['path'])

                getattr(self._move_result, result_type)\
                    .append(file_dict['path'])

    @MoverBase.on_image_moved.getter
    def on_image_moved(self):
        return self._moved_image_event_listeners

    @MoverBase.on_move_finished.getter
    def on_move_finished(self):
        return self._move_finish_event_listeners

    def _validate_dst(self, dst: str) -> None:
        '''
        Without typechecked because it will check arguments manually
        '''
        validate_folder_path(dst, 'destination')
