import io
import contextlib
from unittest.mock import Mock

from pytest import raises
from .utils import with_controller, redirect_stdin, assert_lines_equal


PAD = ' ' * 65
base_scan_output = (
    'Scanning:\n'
    '\r\033[K1: /src/path/1.jpg'
    '\r\033[K2: /src/path/2.jpg'
    '\r\033[K3: /src/path/3.jpg'
    '\r\033[K4: /src/path/4.jpg'
    '\r\033[K5: /src/path/5.mp4'
    '\n'
    '\n'
    f'Movable:      {PAD}4\n'
    f'Not a media:  {PAD}0\n'
    f'No data:      {PAD}1\n'
    f'====={"=" * 70}=====\n'
    f'Total found:  {PAD}5\n'
    '\n'
)


def test_scan_log(container):
    caught_io = io.StringIO()
    argv_args = [None, '-s', '/src/folder', '/dst/folder']
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    with container.exif_data_getter.override(exif_data_getter_mock), \
        contextlib.redirect_stdout(caught_io), \
            with_controller(container, argv_args) as controller,\
            raises(SystemExit) as sys_exit_mock:

        controller.show()

    expected_value = base_scan_output
    assert_lines_equal(caught_io.getvalue(), expected_value)

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
            with_controller(container, argv_args) as controller, \
            raises(SystemExit) as sys_exit_mock:
        controller.show()

    expected_value = base_scan_output + \
        'Do You want to move the 4 files [y/N]: '
    assert_lines_equal(caught_io.getvalue(), expected_value)

    assert sys_exit_mock.type == SystemExit
    assert sys_exit_mock.value.code == 0
