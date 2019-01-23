# -*- coding: utf-8 -*-

import pytest

from ....utils import full_path
from ....core.model.scanner import Scanner
from .fixtures import get_move_map

PATH_TO_TEST_DATA = full_path('tests/data')


class TestScanner:

    def test_scan(self):
        scanner = Scanner()
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

        move_map, no_exif = scanner.scan(PATH_TO_TEST_DATA)

        expected_move_map = get_move_map()
        assert move_map == expected_move_map, 'Should return correct move_map'

        expected_no_exif = [full_path('tests/data/folder-1/1-1.jpg')]
        assert no_exif == expected_no_exif, 'Should return correct no_exif'
