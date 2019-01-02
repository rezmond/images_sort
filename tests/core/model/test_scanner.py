# -*- coding: utf-8 -*-

import os

import pytest

from ....core.model.scanner import Scanner
from .fixtures import get_move_map

ROOT_DIR = os.path.abspath(__file__ + '../../../../../')
PATH_TO_TEST_DATA = os.path.join(ROOT_DIR, 'tests/data')


class TestScanner:

    def test_init(self):
        with pytest.raises(ValueError) as exc_info:
            Scanner(None, None)
        assert 'source' in str(exc_info.value), \
            'Should catch not passed source folder'

        with pytest.raises(ValueError) as exc_info:
            Scanner(PATH_TO_TEST_DATA, None)
        assert 'destination' in str(exc_info.value), \
            'Should catch not passed destination folder'

        assert Scanner(PATH_TO_TEST_DATA, 'tests/out'), 'Should be silent'

        with pytest.raises(ValueError) as exc_info:
            Scanner('test_1', 'test_2')
        assert 'test_1' in str(exc_info.value), \
            'Should catch not existed folder'

    def test_scan(self):
        sorter = Scanner(PATH_TO_TEST_DATA, 'tests/out')
        move_map, no_exif = sorter.scan()

        expected_move_map = get_move_map()
        assert move_map == expected_move_map, 'Should return correct move_map'

        expected_no_exif = [os.path.join(
            ROOT_DIR, 'tests/data/folder-1/1-1.jpg')]
        assert no_exif == expected_no_exif, 'Should return correct no_exif'

    def test_props(self):
        sorter = Scanner(PATH_TO_TEST_DATA, 'tests/out')

        assert sorter.dst_folder == 'tests/out', \
            'Should return correct dst_folder'