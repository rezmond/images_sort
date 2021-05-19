import os
from functools import partial
from typing import Callable, Tuple

from typeguard import typechecked

from core.utils.base import Observable
from core.types import Comparator, FileWay, MoveReport, MoveResult
from ..fs import FsManipulatorBase, FsActions, FolderPathValidatorBase
from .base import MoverBase


class Mover(MoverBase):

    @typechecked
    def __init__(
            self,
            observable_factory: Callable[[], Observable],
            fs_manipulator: FsManipulatorBase,
            comparator: Comparator,
            folder_path_validator: FolderPathValidatorBase
    ) -> None:
        self._fs_manipulator = fs_manipulator
        self._fs_actions = None
        self._move_result = None
        self._dst_folder = None
        self._comparator = comparator
        self._move_finish_event_listeners = observable_factory()
        self._validate_folder_path = folder_path_validator.validate

    @typechecked
    def _cmp_files(
        self,
        dst_dir: str,
        src: str,
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

        :returns: (<can be moved>, <final_path>)
        """
        curr_file_name = os.path.split(src)[1]
        dst_file_path = os.path.join(dst_dir, curr_file_name)

        is_dst_path_busy = self._fs_manipulator.isfile
        if not is_dst_path_busy(dst_file_path):
            return True, dst_file_path

        base_file_name, extension = os.path.splitext(curr_file_name)
        is_dst_file_identical = partial(self._fs_actions.compare, src=src)

        num = 1
        is_new_dst_path_busy = is_dst_path_busy
        while is_new_dst_path_busy(dst_file_path):
            if is_dst_file_identical(dst=dst_file_path):
                return False, dst_file_path

            curr_file_name = f'{base_file_name}_{num}{extension}'
            dst_file_path = os.path.join(dst_dir, curr_file_name)
            num += 1

        return True, dst_file_path

    @typechecked
    def _make_dir_if_not_exists(self, path: str) -> None:
        if not os.path.exists(path):
            self._fs_manipulator.makedirs(path)

    @typechecked
    def move(self,
             file_way: FileWay,
             move_mode: bool = False) -> None:
        '''
        TODO: move the move_mode initialisation to a method
        '''

        self._fs_actions = FsActions(
            self._fs_manipulator, self._comparator, move_mode, move_mode)

        full_dst = os.path.join(self._dst_folder, file_way.dst)
        self._make_dir_if_not_exists(full_dst)
        final_dst = self._move_by_cmp(file_way.src, full_dst)

        self._move_finish_event_listeners.update(
            MoveReport(
                file_way=FileWay(
                    src=file_way.src,
                    dst=file_way.dst,
                    full_dst=final_dst,
                    type=file_way.type,
                ), result=self._move_result))

    @typechecked
    def _move_by_cmp(self, src: str, full_dst: str) -> str:
        to_move, result_path = self._cmp_files(full_dst, src)

        if to_move:
            self._physical_move(src, result_path)
        else:
            self._resolve_conflict(src)

        return result_path

    @typechecked
    def _physical_move(self, src: str, result_path: str) -> None:
        self._fs_actions.move(src, result_path)
        self._move_result = MoveResult.MOVED

    @typechecked
    def _resolve_conflict(self, src: str) -> None:
        self._fs_actions.delete(src)
        self._move_result = MoveResult.ALREADY_EXISTED

    @MoverBase.on_move_finished.getter
    def on_move_finished(self):
        return self._move_finish_event_listeners

    @typechecked
    def set_dst_folder(self, value: str) -> None:
        self._validate_dst(value)
        self._dst_folder = value

    def _validate_dst(self, dst: str) -> None:
        '''
        Without typechecked because it will check arguments manually
        '''
        self._validate_folder_path(dst, 'destination')
