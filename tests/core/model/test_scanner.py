# -*- coding: utf-8 -*-

import pytest
from unittest.mock import call, Mock

from containers import Container
from ....utils import full_path
from ...utils import assert_dict_equal
from .fixtures import get_move_map

PATH_TO_TEST_DATA = full_path('tests/data')


@pytest.fixture
def container():
    ioc = Container()
    yield ioc


class TestScanner:

    def test_scan(self, container):
        scanner = container.scanner()

        with pytest.raises(TypeError) as exc_info:
            scanner.scan(None)
        assert str(exc_info.value) == 'type of argument "src_folder_path" '\
            'must be str; got NoneType instead', \
            'Should catch not passed source folder'

        with pytest.raises(ValueError) as exc_info:
            scanner.scan('test_1')
        assert 'absolute' in str(exc_info.value), \
            'Should catch not absolute the source folder path'

        with pytest.raises(ValueError) as exc_info:
            scanner.scan(full_path('test_1'))
        assert 'test_1' in str(exc_info.value), \
            'Should catch not existed folder'

        scanner.scan(PATH_TO_TEST_DATA)
        move_map, no_data, not_images = scanner.get_data()
        print("move_map, no_data, not_images", move_map, no_data, not_images)

        expected_move_map = get_move_map()
        assert_dict_equal(move_map, expected_move_map,
                          'Should return correct move_map')

        expected_no_exif = [
            full_path('tests/data/video1.mp4'),
            full_path('tests/data/folder-1/1-1.jpg'),
        ]
        assert no_data == expected_no_exif, 'Should return correct no_data'

        expected_not_media = []
        assert not_images == expected_not_media, \
            'Should return correct not_media'

    def test_found_items(self, container):
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
