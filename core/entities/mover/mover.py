import os
from functools import partial
from typing import Callable, Tuple

from typeguard import typechecked

from core.utils.base import Observable
from core.types import Comparator, FileWay, MoveReport, MoveResult
from ..fs import FsManipulatorBase, FsActions
from .base import MoverBase


class Mover(MoverBase):

    @typechecked
    def __init__(
            self,
            observable_factory: Callable[[], Observable],
            fs_manipulator: FsManipulatorBase,
            comparator: Comparator,
            validate_folder_path: Callable[[str, str], None]
    ) -> None:
        self._fs_manipulator = fs_manipulator
        self._fs_actions = None
        self._move_result = None
        self._comparator = comparator
        self._move_finish_event_listeners = observable_factory()
        self._validate_folder_path = validate_folder_path

    @typechecked
    def _cmp_files(
        self,
        dst_dir: str,
        src: str,
    ) -> Tuple[bool, str]:
        """
        TODO: refactor the method

        Check the destination folder for already existed files with the
        same names.

        If a file exists and it is identical, then the current method
        will return fully path to target folder with the False value of
        the first argument.

        If a file with that name exists but it is not identical, then the
        current method will rename the target file name added a number til
        the name will unique.
        """
        curr_file_name = os.path.split(src)[1]
        dst_file_path = os.path.join(dst_dir, curr_file_name)

        if not self._fs_manipulator.isfile(dst_file_path):
            return True, dst_file_path

        base_file_name, extension = os.path.splitext(curr_file_name)
        compare = partial(self._fs_actions.compare, src=src)

        num = 1
        while self._fs_manipulator.isfile(dst_file_path):
            # TODO: cover that line by tests
            if compare(dst=dst_file_path):
                return False, dst_file_path

            curr_file_name = f'{base_file_name}_{num}{extension}'
            dst_file_path = os.path.join(dst_dir, curr_file_name)
            num += 1

        return True, dst_file_path

    @typechecked
    def _make_dir_if_not_exists(self, path: str) -> None:
        """Если целевой папки не было создано"""
        if not os.path.exists(path):
            self._fs_manipulator.makedirs(path)

    @typechecked
    def move(self,
             file_way: FileWay,
             dst_folder: str,
             move_mode: bool = False) -> None:
        self._validate_dst(dst_folder)
        self._fs_actions = FsActions(
            self._fs_manipulator, self._comparator, move_mode, move_mode)

        full_dst = os.path.join(dst_folder, file_way.dst)
        self._make_dir_if_not_exists(full_dst)
        self._move_by_cmp(file_way.src, full_dst)

        self._move_finish_event_listeners.update(
            MoveReport(file_way=file_way, result=self._move_result))

    @typechecked
    def _move_by_cmp(self, src: str, full_dst: str) -> None:
        to_move, result_path = self._cmp_files(full_dst, src)

        if to_move:
            self._physical_move(src, result_path)
            return

        self._resolve_conflict(src)

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

    def _validate_dst(self, dst: str) -> None:
        '''
        Without typechecked because it will check arguments manually
        '''
        self._validate_folder_path(dst, 'destination')
