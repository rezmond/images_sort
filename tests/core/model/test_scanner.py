# -*- coding: utf-8 -*-

import pytest

from ....utils import full_path
from ....core.model.scanner import Scanner
from .fixtures import get_move_map

PATH_TO_TEST_DATA = full_path('tests/data')


class TestScanner:

    def test_init(self):
        with pytest.raises(ValueError) as exc_info:
            Scanner(None)
        assert 'source' in str(exc_info.value), \
            'Should catch not passed source folder'

        assert Scanner(PATH_TO_TEST_DATA), 'Should be silent'

        with pytest.raises(ValueError) as exc_info:
            Scanner('test_1')
        assert 'absolute' in str(exc_info.value), \
            'Should catch not absolute the source folder path'

        with pytest.raises(ValueError) as exc_info:
            Scanner(full_path('test_1'))
        assert 'test_1' in str(exc_info.value), \
            'Should catch not existed folder'

    def test_scan(self):
        sorter = Scanner(PATH_TO_TEST_DATA)
        move_map, no_exif = sorter.scan()

        expected_move_map = get_move_map()
        assert move_map == expected_move_map, 'Should return correct move_map'

        expected_no_exif = [full_path('tests/data/folder-1/1-1.jpg')]
        assert no_exif == expected_no_exif, 'Should return correct no_exif'
