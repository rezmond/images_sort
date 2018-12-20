# -*- coding: utf-8 -*-

from unittest import mock

import pytest

from ...core.sorter import Sorter


class TestSorter:

    def test_init(self):
        with pytest.raises(ValueError) as exc_info:
            Sorter(None, None)
        assert 'source' in str(exc_info.value), \
            'Should catch not passed source folder'

        with pytest.raises(ValueError) as exc_info:
            Sorter('test_1', None)
        assert 'destination' in str(exc_info.value), \
            'Should catch not passed destination folder'

        with mock.patch('os.path.isdir') as mocked_is_dir:
            mocked_is_dir.side_effect = (True, True)
            Sorter('test_1', 'test_2')

        with pytest.raises(ValueError) as exc_info:
            Sorter('test_1', 'test_2')
        assert 'test_1' in str(exc_info.value), \
            'Should catch not existed folder'

    @mock.patch('os.path.isfile', return_value=True)
    @mock.patch('os.listdir', return_value=iter((
        'image-1.jpg',
        'image-2.jpeg',
        'image-3.jpeg',
        'image-4.png',
        'image-5.m4a',
        'image-6.3gp',
    )))
    @mock.patch('os.path.isdir', side_effect=(True, True))
    def test_scan(self, isdir, listdir, isfile):
        sorter = Sorter('test_1', 'test_2')
        sorter.scan()
