# -*- coding: utf-8 -*-

from unittest.mock import patch, call

import pytest

from ...core.sorter import Sorter


class TestSorter:

    def test_init(self):
        with pytest.raises(ValueError) as exc_info:
            Sorter(None, None)
        assert 'source' in str(exc_info.value), \
            'Should catch not passed source folder'

        with pytest.raises(ValueError) as exc_info:
            Sorter('tests/data', None)
        assert 'destination' in str(exc_info.value), \
            'Should catch not passed destination folder'

        assert Sorter('tests/data', 'tests/out'), 'Should be silent'

        with pytest.raises(ValueError) as exc_info:
            Sorter('test_1', 'test_2')
        assert 'test_1' in str(exc_info.value), \
            'Should catch not existed folder'

    def test_move(self):
        sorter = Sorter('tests/data', 'tests/out')
        sorter.scan()

        with patch('shutil.copy2') as patched_copy:
            sorter.move()

        calls = [
            call('tests/data/1.jpg', 'tests/out/2017/winter (begin)/1.jpg'),
            call('tests/data/2.jpg', 'tests/out/2017/spring/2.jpg'),
            call('tests/data/3.jpg', 'tests/out/2017/summer/3.jpg'),
            call('tests/data/4.jpg', 'tests/out/2017/winter (end)/4.jpg'),
        ]
        patched_copy.assert_has_calls(calls, any_order=True)
