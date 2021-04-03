import os
import contextlib
from datetime import date
from unittest.mock import call, Mock

import pytest
import yaml

from core.entities import DateExtractorBase, FolderExtractorBase
from core.types import FileDescriptor
from core.utils.base import Observable
from utils import full_path
from ...utils import assert_dict_equal

PATH_TO_TEST_DATA = full_path('tests/data')


@pytest.fixture
def expected_move_map():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, './fixtures/move_map.yml')
    with open(file_path, 'r') as file_:
        move_map = yaml.full_load(file_)

    for year_values in move_map.values():
        for preiod_name, period_values in year_values.items():
            year_values[preiod_name] = [
                FileDescriptor(
                    value['path'],
                    value['name']
                ) for value in period_values
            ]

    return move_map


def get_scanner(container, **kwargs):
    mocks = {**{
        'date_extractor': Mock(spec=DateExtractorBase),
        'observable': Mock(spec=Observable),
        'fs_manipulator': Mock(spec=FolderExtractorBase),
        'validator': Mock(),
    }, **kwargs}
    with container.date_extractor.override(mocks['date_extractor']),\
            container.observable.override(mocks['observable']),\
            container.fs_manipulator.override(mocks['fs_manipulator']),\
            container.folder_path_validator.override(mocks['validator']):
        scanner = container.scanner()
    return scanner


def test_scan_no_path_error(container):
    scanner = get_scanner(container)

    with pytest.raises(TypeError) as exc_info:
        scanner.scan(None)

    assert str(exc_info.value) == 'type of argument "src_folder_path" '\
        'must be str; got NoneType instead', \
        'Should catch not passed source folder'


def test_scan_path_validation_error(container):
    validator_mock = Mock(side_effect=ValueError('test message'))
    scanner = get_scanner(container, validator=validator_mock)

    with pytest.raises(ValueError) as exc_info:
        scanner.scan('/test_1')

    assert str(exc_info.value) == 'test message',\
        'Should raise validation errors'


def test_scan(container, expected_move_map):
    get_date_mock = {
        '/test/path/1.jpg': date.fromisoformat('2017-01-15'),
        '/test/path/2.jpg': date.fromisoformat('2017-03-14'),
        '/test/path/3.jpg': date.fromisoformat('2017-06-20'),
        '/test/path/5.jpg': date.fromisoformat('2017-12-02'),
        '/test/path/4.jpg': date.fromisoformat('2017-12-30'),
        '/test/path/folder-1/1-1.jpg': None,
        '/test/path/video1.mp4': None,
    }.__getitem__
    date_extractor_mock = Mock(spec=DateExtractorBase, **{
        'is_allowed_extension.return_value': True,
        'get_date': get_date_mock,
    })
    fs_manipulator_mock = Mock(spec=FolderExtractorBase, **{
        'folder_to_file_pathes.return_value': (
            ('1.jpg', '/test/path/1.jpg'),
            ('2.jpg', '/test/path/2.jpg'),
            ('3.jpg', '/test/path/3.jpg'),
            ('5.jpg', '/test/path/5.jpg'),
            ('4.jpg', '/test/path/4.jpg'),
            ('1-1.jpg', '/test/path/folder-1/1-1.jpg'),
            ('video1.mp4', '/test/path/video1.mp4'),
        ),
    })
    scanner = get_scanner(
        container,
        date_extractor=date_extractor_mock,
        fs_manipulator=fs_manipulator_mock,
    )

    scanner.scan('')
    scanned = scanner.get_data()

    assert_dict_equal(scanned.move_map, expected_move_map,
                      'Should return correct move_map')

    expected_no_exif = [
        '/test/path/video1.mp4',
        '/test/path/folder-1/1-1.jpg',
    ]
    assert scanned.no_data == expected_no_exif, 'Should return correct no_data'

    expected_not_media = []
    assert scanned.not_media == expected_not_media, \
        'Should return correct not_media'


def test_found_items(container):
    scanner = container.scanner()
    handler_mock = Mock()
    scanner.on_file_found += handler_mock
    scanner.scan(PATH_TO_TEST_DATA)

    expected_calls = [
        call(full_path('tests/data/2.jpg')),
        call(full_path('tests/data/1.jpg')),
        call(full_path('tests/data/3.jpg')),
        call(full_path('tests/data/video1.mp4')),
        call(full_path('tests/data/5.jpg')),
        call(full_path('tests/data/folder-1/1-1.jpg')),
        call(full_path('tests/data/4.jpg')),
    ]

    handler_mock.assert_has_calls(expected_calls, any_order=True)


def test_filling_mot_media(container):
    date_extractor_mock = Mock(spec=DateExtractorBase, **{
        'is_allowed_extension.return_value': False
    })
    observable_mock = Mock(spec=Observable)
    fs_manipulator_mock = Mock(spec=FolderExtractorBase, **{
        'folder_to_file_pathes.return_value': (('', 'b'),)
    })
    with container.date_extractor.override(date_extractor_mock),\
            container.observable.override(observable_mock),\
            container.fs_manipulator.override(fs_manipulator_mock),\
            container.folder_path_validator.override(Mock()):
        scanner = container.scanner()
    scanner.scan('/test/path')
    result = scanner.get_data()
    assert result.move_map == {}
    assert result.no_data == []
    assert result.not_media == ['b']
