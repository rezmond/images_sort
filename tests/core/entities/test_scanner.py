from datetime import date
from unittest.mock import call, Mock

import pytest

from core.entities import DateExtractorBase, FolderExtractorBase, MoveMapBase
from core.types import FileWay, MoveType
from core.utils.base import Observable

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


def get_fs_manipulator_mock():
    return Mock(spec=FolderExtractorBase, **{
        'folder_to_file_pathes.return_value': base_pathes,
    })


def get_scanner(container, **kwargs):
    mocks = {**{
        'date_extractor': Mock(spec=DateExtractorBase),
        'observable': Mock(spec=Observable),
        'fs_manipulator': Mock(spec=FolderExtractorBase),
        'move_map': Mock(spec=MoveMapBase),
        'validator': Mock(),
    }, **kwargs}
    with container.date_extractor.override(mocks['date_extractor']),\
            container.observable.override(mocks['observable']),\
            container.fs_manipulator.override(mocks['fs_manipulator']),\
            container.move_map.override(mocks['move_map']),\
            container.folder_path_validator.override(mocks['validator']):
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
    validator_mock = Mock(side_effect=ValueError('test message'))
    scanner = get_scanner(container, validator=validator_mock)

    with pytest.raises(ValueError) as exc_info:
        list(scanner.scan('/test_1'))

    assert str(exc_info.value) == 'test message',\
        'Should raise validation errors'


def test_scan(container):
    get_date_mock = dict(base_path_map).__getitem__
    date_extractor_mock = Mock(spec=DateExtractorBase, **{
        'is_allowed_extension.return_value': True,
        'get_date': get_date_mock,
    })

    def get_dst_path_mock(d):
        return f'dst path of "{d}"'

    move_map_mock = Mock(spec=MoveMapBase, get_dst_path=get_dst_path_mock)
    scanner = get_scanner(
        container,
        date_extractor=date_extractor_mock,
        fs_manipulator=get_fs_manipulator_mock(),
        move_map=move_map_mock,
    )

    scanned = list(scanner.scan(''))

    expected_scanned = [
        FileWay(
            src=x,
            dst=get_dst_path_mock(get_date_mock(x)),
            type=MoveType.MEDIA)
        if get_date_mock(x)
        else FileWay(src=x, dst=None, type=MoveType.NO_DATA)
        for x in base_pathes
    ]

    assert scanned == expected_scanned


def test_found_items(container):
    fs_manipulator_mock = get_fs_manipulator_mock()
    scanner = get_scanner(
        container, fs_manipulator=fs_manipulator_mock, observable=Observable())
    handler_mock = Mock()
    scanner.on_file_found += handler_mock

    list(scanner.scan(''))

    expected_calls = list(map(call, base_pathes))
    handler_mock.assert_has_calls(expected_calls)


def test_filling_not_media(container):
    scanner = get_scanner(
        container,
        date_extractor=Mock(spec=DateExtractorBase, **{
            'is_allowed_extension.return_value': False
        }),
        fs_manipulator=Mock(spec=FolderExtractorBase, **{
            'folder_to_file_pathes.return_value': ('/no/media/file.path',)
        }),
    )

    result = list(scanner.scan(''))
    assert result == [
        FileWay(src='/no/media/file.path', type=MoveType.NO_MEDIA)]
