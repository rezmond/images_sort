from datetime import date
from unittest.mock import Mock
from functools import partial

import pytest

from core.entities import (
    DateExtractorBase,
    FolderExtractorBase,
    FolderCheckerBase,
    MoveMapBase,
)
from core.entities.exceptions import FolderNotFoundError
from core.types import FileWay, MoveType
from core.utils.base import Observable
from tests.utils import overrides


class FsManipulatorCompilation(FolderCheckerBase, FolderExtractorBase):
    pass


base_path_map = (
    ('/src/path/1.jpg', date.fromisoformat('2017-01-15')),
    ('/src/path/2.jpg', date.fromisoformat('2017-03-14')),
    ('/src/path/3.jpg', date.fromisoformat('2017-06-20')),
    ('/src/path/5.jpg', date.fromisoformat('2017-12-02')),
    ('/src/path/4.jpg', date.fromisoformat('2017-12-30')),
    ('/src/path/folder-1/1-1.jpg', None),
    ('/src/path/video1.mp4', None),
)

base_pathes = [path for (path, _) in base_path_map]


def get_fs_manipulator_mock(**options):
    return Mock(spec=FsManipulatorCompilation, **{
        'folder_to_file_pathes.return_value': base_pathes,
        **options,
    })


def get_scanner(container, **kwargs):
    mocks = {**{
        'date_extractor': Mock(spec=DateExtractorBase),
        'observable': Mock(spec=Observable),
        'fs_manipulator': Mock(spec=FsManipulatorCompilation),
        'move_map': Mock(spec=MoveMapBase),
    }, **kwargs}
    with overrides(container, **mocks):
        scanner = container.scanner()
    return scanner


def test_scan_no_path_error(container):
    scanner = get_scanner(container)

    with pytest.raises(TypeError) as exc_info:
        list(scanner.scan(None))

    assert str(exc_info.value) == 'type of argument "src_folder" '\
        'must be str; got NoneType instead', \
        'Should catch not passed source folder'


def test_scan_path_validation_error(container):
    fs_manipulator_mock = Mock(
        spec=FsManipulatorCompilation,
        **{'isfolder.return_value': False},
    )
    scanner = get_scanner(container, fs_manipulator=fs_manipulator_mock)

    with pytest.raises(FolderNotFoundError) as exc_info:
        list(scanner.scan('/test_1'))

    assert 'source' in str(exc_info.value)


def test_scan(container):
    get_date_mock = dict(base_path_map).__getitem__
    date_extractor_mock = Mock(spec=DateExtractorBase, **{
        'is_allowed_extension.return_value': True,
        'get_date': get_date_mock,
    })
    fs_manipulator_mock = get_fs_manipulator_mock(
        **{'isfolder.return_value': True},
    )

    def get_dst_path_mock(d):
        return f'dst path of "{d}"'

    def assert_moved_to_correct_dir(scan_generator):
        for i, report in enumerate(scan_generator):
            path = base_pathes[i]
            file_way = partial(FileWay, src=path)
            date_by_path = get_date_mock(path)

            if date_by_path:
                expected = file_way(
                    dst=get_dst_path_mock(date_by_path),
                    type=MoveType.MEDIA
                )
            else:
                expected = file_way(dst=None, type=MoveType.NO_DATA)

            assert report == expected

    move_map_mock = Mock(spec=MoveMapBase, get_dst_path=get_dst_path_mock)

    scanner = get_scanner(
        container,
        date_extractor=date_extractor_mock,
        fs_manipulator=fs_manipulator_mock,
        move_map=move_map_mock,
    )

    scan_generator = scanner.scan('/test')

    assert_moved_to_correct_dir(scan_generator)


def test_filling_not_media(container):
    scanner = get_scanner(
        container,
        date_extractor=Mock(spec=DateExtractorBase, **{
            'is_allowed_extension.return_value': False
        }),
        fs_manipulator=get_fs_manipulator_mock(**{
            'folder_to_file_pathes.return_value': ('/no/media/file.path',)
        }),
    )

    result = list(scanner.scan('/test'))

    assert result == [
        FileWay(src='/no/media/file.path', type=MoveType.NO_MEDIA)]
