import io
import contextlib
from typing import Iterable

from typeguard import typechecked
from unittest.mock import Mock, patch

from core.types import MoveReport
from core.mvc.views import ConsoleView
from utils import pipe
from .utils import (
    base_pathes,
    redirect_stdin,
    with_controller,
    assert_lines_equal,
    FsManipulatorCompilation,
)


class ConsoleViewMock(ConsoleView):
    @typechecked
    def move_in_context(
            self, moved_reports: Iterable[MoveReport], length: int):
        return moved_reports


PAD = ' ' * 60


def test_creates_target_folder(container):
    is_dst_folder_existed = False

    def false_if_dst(path):
        if path == '/src/folder':
            return True
        return is_dst_folder_existed

    def isfile_mock(_):
        return False

    def create_folder(_):
        nonlocal is_dst_folder_existed
        is_dst_folder_existed = True

    def comparator(_, __):
        return False

    caught_io = io.StringIO()
    input_io = io.StringIO('y\n')
    argv_args = [None, '-m', '-v 1', '/src/folder', '/dst/folder']
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    fs_manipulator = Mock(spec=FsManipulatorCompilation, **{
        'folder_to_file_pathes.return_value': base_pathes,
        'isfolder': false_if_dst,
        'isfile': isfile_mock,
        'create_folder': create_folder,
    })

    caught_report_stings = []

    def move_in_context_mock(gen, length, item_show_func):
        assert length == 4

        moved = list(
            map(pipe(item_show_func, caught_report_stings.append), gen))
        mock = Mock()
        mock.__enter__ = Mock(return_value=moved)
        mock.__exit__ = Mock(return_value=False)

        return mock

    with container.exif_data_getter.override(
        exif_data_getter_mock
    ), contextlib.redirect_stdout(
        caught_io
    ), redirect_stdin(
        input_io
    ), with_controller(
        container, argv_args,
        fs_manipulator=fs_manipulator,
        comparator=comparator
    ) as console:
        view = container.view()
        view.move_in_context = move_in_context_mock
        console.show()

    expected_stdout = (
        'The "/dst/folder" folder does not exist.\n'
        'Do You want to create it [y/N]: \n'
        f'Have been moved:   {PAD}4\n'
        f'Already existed:   {PAD}0\n'
        f'Not a media:       {PAD}0\n'
        f'No data:           {PAD}0\n'
    )
    assert_lines_equal(
        caught_io.getvalue().split('\n')[-7:],
        expected_stdout
    )

    expected_str_reports = (
        '\r\x1b[K/src/path/1.jpg -> /dst/folder/2000/winter (begin)/1.jpg\n'
        '\r\x1b[K/src/path/2.jpg -> /dst/folder/2000/winter (begin)/2.jpg\n'
        '\r\x1b[K/src/path/3.jpg -> /dst/folder/2000/winter (begin)/3.jpg\n'
        '\r\x1b[K/src/path/4.jpg -> /dst/folder/2000/winter (begin)/4.jpg\n'
    )
    assert_lines_equal(expected_str_reports, expected_str_reports)
