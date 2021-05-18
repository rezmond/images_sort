import io
import sys
import contextlib
from datetime import date
from unittest.mock import patch, Mock

from pytest import raises

from core.entities import (
    FolderExtractorBase,
    FsManipulatorBase,
)
from core.system_interfaces import FolderCheckerBase


class FsManipulatorCompilation(
        FolderCheckerBase, FsManipulatorBase, FolderExtractorBase):
    pass


base_path_map = (
    ('/src/path/1.jpg', date.fromisoformat('2017-01-15')),
    ('/src/path/2.jpg', date.fromisoformat('2017-03-14')),
    ('/src/path/3.jpg', date.fromisoformat('2017-06-20')),
    ('/src/path/4.jpg', date.fromisoformat('2017-12-30')),
)

base_pathes = [path for (path, _) in base_path_map]


def get_fs_manipulator_mock():
    return Mock(spec=FsManipulatorCompilation, **{
        'folder_to_file_pathes.return_value': base_pathes,
    })


@contextlib.contextmanager
def with_presenter(container, argv_args):
    fs_manipulator_mock = get_fs_manipulator_mock()
    with patch('sys.argv', argv_args), \
            container.fs_manipulator.override(fs_manipulator_mock):
        controller = container.controller()
        view = container.view()
        view.set_controller(controller)
        presenter = container.presenter()
        yield presenter


@contextlib.contextmanager
def redirect_stdin(new_stdin):
    original_stdin = sys.stdin
    sys.stdin = new_stdin
    yield
    sys.stdin = original_stdin


def assert_lines_equal(actual, expected):
    actual_lines = actual.splitlines()
    expected_lines = expected.splitlines()

    assert len(actual_lines) == len(expected_lines)
    for actual_line, expected_line in zip(actual_lines, expected_lines):
        assert actual_line == expected_line


def test_scan_log(container):
    caught_io = io.StringIO()
    argv_args = [None, '-s', '/src/folder', '/dst/folder']
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    with container.exif_data_getter.override(exif_data_getter_mock), \
        contextlib.redirect_stdout(caught_io), \
            with_presenter(container, argv_args) as presenter,\
            raises(SystemExit) as sys_exit_mock:

        presenter.show()

    pad = ' ' * 65
    scanning_expect = (
        'Scanning:\n'
        '\r\033[K1: /src/path/1.jpg'
        '\r\033[K2: /src/path/2.jpg'
        '\r\033[K3: /src/path/3.jpg'
        '\r\033[K4: /src/path/4.jpg'
        '\n'
        f'Movable:      {pad}4\n'
        f'Not a media:  {pad}0\n'
        f'No data:      {pad}0\n'
        f'====={"=" * 70}=====\n'
        f'Total found:  {pad}4\n'
        '\n'
    )

    assert_lines_equal(caught_io.getvalue(), scanning_expect)

    assert sys_exit_mock.type == SystemExit
    assert sys_exit_mock.value.code == 0


def test_cancel_move_log(container):
    caught_io = io.StringIO()
    input_io = io.StringIO('n\n')
    argv_args = [None, '/src/folder', '/dst/folder']
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    with container.exif_data_getter.override(exif_data_getter_mock), \
        contextlib.redirect_stdout(caught_io), \
        redirect_stdin(input_io), \
            with_presenter(container, argv_args) as presenter, \
            raises(SystemExit) as sys_exit_mock:
        presenter.show()

    expected_message = 'Do You want to move the 4 files [y/N]: '
    last_line = caught_io.getvalue().splitlines()[-1]
    assert last_line == expected_message

    assert sys_exit_mock.type == SystemExit
    assert sys_exit_mock.value.code == 0
