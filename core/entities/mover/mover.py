# -*- coding: utf-8 -*-

import os
from functools import partial
from typing import Callable, Dict, Tuple

from typeguard import typechecked

from core.utils.base import Observable
from core.types import BlocksType, Comparator, ScanResult, YearType
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

    @typechecked
    def _cmp_files(
        self,
        dst_dir: str,
        file_dict: Dict[str, str]
    ) -> Tuple[bool, str]:
        """
        Check the destination folder for already existed files with the
        same names.

        If a file exists and it is identical, then the current method
        will return fully path to target folder with the False value of
        the first argument.

        If a file with that name exists but it is not identical, then the
        current method will rename the target file name added a number til
        the name will unique.
        """
        curr_file_name = os.path.split(file_dict['path'])[1]
        dst_file_path = os.path.join(dst_dir, curr_file_name)

        if not os.path.isfile(dst_file_path):
            return True, dst_file_path

        base_file_name, extension = os.path.splitext(curr_file_name)
        compare = partial(self._fs_actions.compare, dst=dst_file_path)

        num = 1
        while os.path.isfile(dst_file_path):
            if compare(file_dict['path']):
                return False, dst_file_path

            curr_file_name = f'{base_file_name}_{num}{extension}'
            dst_file_path = os.path.join(dst_dir, curr_file_name)
            num += 1

        return True, dst_file_path

    def _make_dir_if_not_exists(self, path):
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

            self._make_dir_if_not_exists(dst_dir_path)
            self._move_by_cmp(m_value, dst_dir_path)

    @typechecked
    def _move_by_cmp(self, m_value: BlocksType, dst_dir_path: str) -> None:
        for file_dict in m_value:
            to_move, result_path = self._cmp_files(dst_dir_path, file_dict)

            if to_move:
                self._physical_move(file_dict['path'], result_path)
                continue

            self._resolve_conflict(file_dict['path'])

    @typechecked
    def _physical_move(self, path: str, result_path: str) -> None:
        self._fs_actions.move(path, result_path)
        self._moved_image_event_listeners.update((path, result_path))
        self._move_result.moved.append(path)

    @typechecked
    def _resolve_conflict(self, path: str) -> None:
        self._fs_actions.delete(path)
        self._move_result.already_exists.append(path)

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
