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
def with_controller(container, argv_args):
    fs_manipulator_mock = get_fs_manipulator_mock()
    with patch('sys.argv', argv_args), \
            container.fs_manipulator.override(fs_manipulator_mock):
        controller = container.controller()
        view = container.view()
        view.set_controller(controller)
        controller.set_input_interactor(view)
        yield controller


def test_scan_log(container):
    caught_io = io.StringIO()
    argv_args = [None, '-s', '/src/folder', '/dst/folder']
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    with container.exif_data_getter.override(exif_data_getter_mock), \
        contextlib.redirect_stdout(caught_io), \
            with_controller(container, argv_args) as controller:
        controller.show()

    expect = 'Scanning:\n' + ''.join(
        starmap('\r\033[K{}: {}'.format, enumerate(base_pathes, 1))
    ) + '\n'

    assert caught_io.getvalue() == expect
