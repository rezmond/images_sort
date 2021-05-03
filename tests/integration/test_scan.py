import io
import contextlib
from datetime import date
from unittest.mock import patch, Mock
from itertools import starmap

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
            with_presenter(container, argv_args) as presenter:
        presenter.show()

    scanning_expect = 'Scanning:\n' + ''.join(
        starmap('\r\033[K{}: {}'.format, enumerate(base_pathes, 1))
    ) + '\n'

    assert_lines_equal(caught_io.getvalue()[
                       :len(scanning_expect)], scanning_expect)

    pad = ' ' * 65
    report_expect_lines = (
        f'Movable:      {pad}4\n'
        f'Not a media:  {pad}0\n'
        f'No data:      {pad}0\n'
        f'{"=" * 80}\n'
        f'Total found:  {pad}4\n'
        '\n'
    )
    scan_report_actual = caught_io.getvalue()[len(scanning_expect):]
    assert_lines_equal(scan_report_actual, report_expect_lines)
