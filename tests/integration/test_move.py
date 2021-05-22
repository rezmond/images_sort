import io
import contextlib

from unittest.mock import Mock

from .utils import (
    base_pathes,
    redirect_stdin,
    with_presenter,
    assert_lines_equal,
    FsManipulatorCompilation,
)


def test_creates_target_folder(container):
    def false_if_dst(path):
        if path == '/src/folder':
            return True
        return False

    caught_io = io.StringIO()
    input_io = io.StringIO('n\n')
    argv_args = [None, '-m', '/src/folder', '/dst/folder']
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    fs_manipulator = Mock(spec=FsManipulatorCompilation, **{
        'folder_to_file_pathes.return_value': base_pathes,
        'isfolder': false_if_dst,
    })
    with container.exif_data_getter.override(
        exif_data_getter_mock
    ), contextlib.redirect_stdout(
        caught_io
    ), redirect_stdin(
        input_io
    ), with_presenter(
        container, argv_args, fs_manipulator=fs_manipulator
    ) as presenter:
        presenter.show()

    expected_value = (
        'The "/dst/folder" folder does not exist.\n'
        'Do You want to create it [y/N]: '
    )

    assert_lines_equal(caught_io.getvalue().splitlines()[-2:], expected_value)
