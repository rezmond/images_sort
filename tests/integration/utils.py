import contextlib
import sys
from datetime import date
from unittest.mock import patch, Mock

from core.entities import (
    FolderExtractorBase,
    FsManipulatorBase,
)

base_path_map = (
    ('/src/path/1.jpg', date.fromisoformat('2017-01-15')),
    ('/src/path/2.jpg', date.fromisoformat('2017-03-14')),
    ('/src/path/3.jpg', date.fromisoformat('2017-06-20')),
    ('/src/path/4.jpg', date.fromisoformat('2017-12-30')),
    ('/src/path/5.mp4', None),
)

base_pathes = [path for (path, _) in base_path_map]


class FsManipulatorCompilation(FsManipulatorBase, FolderExtractorBase):
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
        'isfolder.return_value': True,
    })


def get_comparator_mock():
    return Mock(sreturn_value=False)


@contextlib.contextmanager
def with_controller(container, argv_args, **mocks):
    fs_manipulator_mock = mocks.get(
        'fs_manipulator', get_fs_manipulator_mock())
    comparator_mock = mocks.get(
        'comparator', get_comparator_mock())
    with patch('sys.argv', argv_args), \
            container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(comparator_mock):
        view = container.view()

        controller = container.controller()
        controller.set_io_interactor(view)

        model = container.model()
        model.set_output_boundary(controller)

        controller = container.controller()
        yield controller


def assert_lines_equal(actual, expected):
    if isinstance(actual, list):
        actual_lines = actual
    else:
        actual_lines = actual.split('\n')

    expected_lines = expected.split('\n')

    assert len(actual_lines) == len(expected_lines)
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        assert actual_line == expected_line, (
            'the strings are not equal.\n'
            f'First:\t "{actual_line}"\n'
            f'Second:\t "{expected_line}"'
        )
