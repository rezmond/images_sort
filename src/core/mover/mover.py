import os
from typing import Tuple

from typeguard import typechecked

from libs import Either
from src.core.scanners.base import TargetFolderScannerBase
from src.types import Comparator, FileWay, MoveReport, MoveResult

from ..fs import FolderPathValidator, FsActions, FsManipulatorBase
from .base import MoverBase


class Mover(MoverBase):
    @typechecked
    def __init__(
        self,
        fs_manipulator: FsManipulatorBase,
        comparator: Comparator,
        target_folder_scanner: TargetFolderScannerBase,
    ) -> None:
        self._fs_manipulator = fs_manipulator
        self._fs_actions = None
        self._dst_folder = None
        self._comparator = comparator
        self._folder_path_validator = FolderPathValidator(self._fs_manipulator)
        self._target_folder_scanner = target_folder_scanner

    @typechecked
    def _cmp_files(
        self,
        src: str,
        dst_dir: str,
    ) -> Tuple[bool, str]:
        """
        Check the destination folder for already existed files with the
        same names.

        If a file exists and it is identical, then the current method
        will return full path to target folder with the False value of
        the first argument.

        If a file with that name exists but it is not identical, then the
        current method will rename the target file name added a number til
        the name will unique.

        :returns: (can_be_moved: bool, final_path: str)
        """
        curr_file_name = os.path.basename(src)
        dst_file_path = os.path.join(dst_dir, curr_file_name)

        if self._target_folder_scanner.detect_duplicates(src):
            return False, dst_file_path

        final_dst_file_path = (
            dst_file_path
            if not self._fs_manipulator.isfile(dst_file_path)
            else self._generate_unique_file_path(src, dst_dir)
        )
        return True, final_dst_file_path

    @typechecked
    def _generate_unique_file_path(self, src: str, dst_dir: str) -> str:
        """Return a full unique file path by appending a number if needed."""

        curr_file_name = os.path.basename(src)
        base_file_name, extension = os.path.splitext(curr_file_name)

        num = 0

        def next_name():
            nonlocal num
            num += 1
            return os.path.join(dst_dir, f'{base_file_name}_{num}{extension}')

        while True:
            dst_file_path = next_name()
            if not self._fs_manipulator.isfile(dst_file_path):
                break

        return dst_file_path

    @typechecked
    def _make_dir_if_not_exists(self, path: str) -> None:
        if not os.path.exists(path):
            self._fs_manipulator.makedirs(path)

    @typechecked
    def move(self, file_way: FileWay, move_mode: bool = False) -> MoveReport:
        """
        TODO: move the move_mode initialization to a method
        """
        assert file_way.dst is not None, (
            f'The file way {file_way} has empty destination.'
        )

        full_dst = os.path.join(self.get_dst_folder(), file_way.dst)

        self._fs_actions = FsActions(
            self._fs_manipulator, self._comparator, move_mode, move_mode
        )

        self._make_dir_if_not_exists(full_dst)
        full_dst, move_result = self._move_by_cmp(file_way.src, full_dst)

        return MoveReport(
            file_way=FileWay(
                src=file_way.src,
                dst=file_way.dst,
                full_dst=full_dst,
                type=file_way.type,
            ),
            result=move_result,
        )

    @typechecked
    def _move_by_cmp(self, src: str, full_dst: str) -> Tuple[str, MoveResult]:
        no_duplicates, final_path = self._cmp_files(src, full_dst)

        if no_duplicates:
            self._physical_move(src, final_path)
            return final_path, MoveResult.MOVED

        self._resolve_duplicate(src)
        return final_path, MoveResult.ALREADY_EXISTED

    @typechecked
    def _physical_move(self, src: str, result_path: str) -> None:
        self._fs_actions.move(src, result_path)

    @typechecked
    def _resolve_duplicate(self, src: str) -> None:
        self._fs_actions.delete(src)

    @typechecked
    def set_dst_folder(self, dst: str) -> Either:
        def do_set(dst: str):
            self._dst_folder = dst

        return self._validate_dst(dst).map(do_set)

    @typechecked
    def get_dst_folder(self) -> str | None:
        return self._dst_folder

    @typechecked
    def create_and_set_dst_folder(self, dst: str) -> None:
        self._fs_manipulator.makedirs(dst)
        self._dst_folder = dst

    def _validate_dst(self, dst: str) -> Either:
        """
        Without typechecked because it will check arguments manually
        """
        return self._folder_path_validator.validate('destination', dst)
