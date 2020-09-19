# -*- coding: utf-8 -*-

import pytest
from unittest.mock import call, Mock

from ....utils import full_path
from ....core.model.scanner import Scanner
from ....core.utils.ioc import InverseOfControlContainer
from ....core.utils.base import Observable
from .fixtures import get_move_map

PATH_TO_TEST_DATA = full_path('tests/data')


def clreate_ioc():
    ioc = InverseOfControlContainer()
    ioc.add('observable', Observable)
    return ioc


class TestScanner:

    def test_scan(self):
        ioc = clreate_ioc()
        scanner = Scanner(ioc)

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
        move_map, no_exif, not_images = scanner.get_data()

        expected_move_map = get_move_map()
        assert move_map == expected_move_map, 'Should return correct move_map'

        expected_no_exif = [full_path('tests/data/folder-1/1-1.jpg')]
        assert no_exif == expected_no_exif, 'Should return correct no_exif'

        expected_not_images = [full_path('tests/data/video1.mp4')]
        assert not_images == expected_not_images, \
            'Should return correct not_images'

    def test_found_items(self):
        ioc = clreate_ioc()
        scanner = Scanner(ioc)
        handler_mock = Mock()
        scanner.on_image_found += handler_mock
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
