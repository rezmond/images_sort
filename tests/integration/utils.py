import contextlib
import sys
from datetime import date
from unittest.mock import patch, Mock


from core.entities import (
    FolderExtractorBase,
    FsManipulatorBase,
)
from core.system_interfaces import FolderCheckerBase

base_path_map = (
    ('/src/path/1.jpg', date.fromisoformat('2017-01-15')),
    ('/src/path/2.jpg', date.fromisoformat('2017-03-14')),
    ('/src/path/3.jpg', date.fromisoformat('2017-06-20')),
    ('/src/path/4.jpg', date.fromisoformat('2017-12-30')),
)

base_pathes = [path for (path, _) in base_path_map]


class FsManipulatorCompilation(
        FolderCheckerBase, FsManipulatorBase, FolderExtractorBase):
    pass


@contextlib.contextmanager
def redirect_stdin(new_stdin):
    original_stdin = sys.stdin
    sys.stdin = new_stdin
    yield
    sys.stdin = original_stdin


def get_fs_manipulator_mock():
    return Mock(spec=FsManipulatorCompilation, **{
        'folder_to_file_pathes.return_value': base_pathes,
    })


@contextlib.contextmanager
def with_presenter(container, argv_args, **mocks):
    fs_manipulator_mock = mocks.get(
        'fs_manipulator', get_fs_manipulator_mock())
    with patch('sys.argv', argv_args), \
            container.fs_manipulator.override(fs_manipulator_mock):
        controller = container.controller()
        view = container.view()
        view.set_controller(controller)
        presenter = container.presenter()
        yield presenter


def assert_lines_equal(actual, expected):
    actual_lines = actual.splitlines()
    expected_lines = expected.splitlines()

    assert len(actual_lines) == len(expected_lines)
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        assert actual_line == expected_line
