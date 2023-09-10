import io
import contextlib

from unittest.mock import call, Mock, patch, mock_open

from tests.utils import get_progressbar_mock
from .utils import (
    base_pathes,
    redirect_stdin,
    with_controller,
    assert_lines_equal,
    FsManipulatorCompilation,
)


PAD = ' ' * 60


def move_line(item):
    return (
        f'\n\x1b[K/src/path/{item}.jpg --> '
        f'/dst/folder/2000/winter (begin)/{item}.jpg\x1b[2A\n'
    )


def test_creates_target_folder(container):
    is_dst_folder_existed = False

    def false_if_dst(path):
        if path == '/src/folder':
            return True
        return is_dst_folder_existed

    def isfile_mock(_):
        return False

    def makedirs(_):
        nonlocal is_dst_folder_existed
        is_dst_folder_existed = True

    def comparator(_, __):
        return False

    caught_io = io.StringIO()
    input_io = io.StringIO('y\ny\n')
    argv_args = [None, '-v 2', '/src/folder', '/dst/folder']
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    fs_manipulator = Mock(spec=FsManipulatorCompilation, **{
        'folder_to_file_pathes.return_value': base_pathes,
        'isfolder': false_if_dst,
        'isfile': isfile_mock,
        'makedirs': makedirs,
    })

    mock_of_open = mock_open()
    progressbar_mock = get_progressbar_mock(len(base_pathes))
    with patch(
        'src.mvc.views.console.console.open', mock_of_open
    ), container.exif_data_getter.override(
        exif_data_getter_mock
    ), contextlib.redirect_stdout(
        caught_io
    ), redirect_stdin(
        input_io
    ), patch('click.progressbar', progressbar_mock), \
        with_controller(
        container, argv_args,
        fs_manipulator=fs_manipulator,
        comparator=comparator
    ) as console:
        console.show()

    expected_stdout = (
        '\n'
        'Do You want to move the 4 files [y/N]: '
        'The "/dst/folder" folder does not exist.\n'
        'Do You want to create it [y/N]: \n'
        '\n'
        '\n'
        '\n'
        f'Have been moved:   {PAD}4\n'
        f'Already existed:   {PAD}0\n'
        f'Not a media:       {PAD}0\n'
        f'No data:           {PAD}1\n'
        f'{"=" * 80}\n'
        'Report was existed in: /dst/folder/report.txt\n'
    ) + ''.join((move_line(1), move_line(2), move_line(3), move_line(4)))

    assert_lines_equal(
        caught_io.getvalue().split('\n')[-21:],
        expected_stdout
    )

    report_file_calls = [
        call('/dst/folder/report.txt', 'w'),
        call().__enter__(),
        call().write('Moved (4):\n'),
        call().write('==========\n'),
        call().write(
            '    /src/path/1.jpg --> /dst/folder/2000/winter (begin)/1.jpg\n'),
        call().write(
            '    /src/path/2.jpg --> /dst/folder/2000/winter (begin)/2.jpg\n'),
        call().write(
            '    /src/path/3.jpg --> /dst/folder/2000/winter (begin)/3.jpg\n'),
        call().write(
            '    /src/path/4.jpg --> /dst/folder/2000/winter (begin)/4.jpg\n'),
        call().write('\n'),
        call().write('Already existed (0):\n'),
        call().write('====================\n'),
        call().write('\n'),
        call().write('Not a media (0):\n'),
        call().write('================\n'),
        call().write('\n'),
        call().write('No data (1):\n'),
        call().write('============\n'),
        call().write('    /src/path/5.mp4\n'),
        call().write('\n'),
        call().__exit__(None, None, None)
    ]

    mock_of_open.assert_has_calls(report_file_calls)
