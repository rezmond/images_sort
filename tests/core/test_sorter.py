# -*- coding: utf-8 -*-

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
