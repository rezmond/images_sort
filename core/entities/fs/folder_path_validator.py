import os

from typeguard import typechecked

from .folder_checker_base import FolderCheckerBase


class FolderPathValidator:

    @typechecked
    def __init__(self, fs_manipulator: FolderCheckerBase) -> None:
        self._fs_manipulator = fs_manipulator

    @typechecked
    def validate(self, param_value: str, param_humanize: str) -> None:

        if not param_value:
            raise ValueError(
                'The "{0}" folder\'s path has not been set.'
                ' Please set the "{0}" folder path and try again.'
                .format(param_humanize))

        if not os.path.isabs(param_value):
            raise ValueError(
                f'The "{param_humanize}" folder path should be absolute,'
                f' but got "{param_value}"')

        if not self._fs_manipulator.isfolder(param_value):
            raise ValueError(
                f'The "{param_value}" folder does not exist')
