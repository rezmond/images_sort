# -*- coding: utf-8 -*-

from unittest.mock import patch, call

import pytest

from ....core.model.scanner import Scanner


class TestScanner:

    def test_init(self):
        with pytest.raises(ValueError) as exc_info:
            Scanner(None, None)
        assert 'source' in str(exc_info.value), \
            'Should catch not passed source folder'

        with pytest.raises(ValueError) as exc_info:
            Scanner('tests/data', None)
        assert 'destination' in str(exc_info.value), \
            'Should catch not passed destination folder'

        assert Scanner('tests/data', 'tests/out'), 'Should be silent'

        with pytest.raises(ValueError) as exc_info:
            Scanner('test_1', 'test_2')
        assert 'test_1' in str(exc_info.value), \
            'Should catch not existed folder'

    @patch('os.makedirs')
    def test_move(self, patched_makedirs):
        sorter = Scanner('tests/data', 'tests/out')
        move_map, no_exif = sorter.scan()

        expected_move_map = {
            '2017': {
                'spring': [{
                    'path': 'tests/data/2.jpg',
                    'name': '2.jpg'
                }],
                'winter (begin)': [{
                    'path': 'tests/data/1.jpg',
                    'name': '1.jpg'
                }],
                'summer': [{
                    'path': 'tests/data/3.jpg',
                    'name': '3.jpg'
                }],
                'winter (end)': [{
                    'path': 'tests/data/4.jpg',
                    'name': '4.jpg'
                }]
            }
        }
        assert move_map == expected_move_map, 'Should return correct move_map'

        expected_no_exif = ['tests/data/folder-1/1-1.jpg']
        assert no_exif == expected_no_exif, 'Should return correct no_exif'

        with patch('shutil.copy2') as patched_copy:
            sorter.move()

        calls = [
            call('tests/data/1.jpg', 'tests/out/2017/winter (begin)/1.jpg'),
            call('tests/data/2.jpg', 'tests/out/2017/spring/2.jpg'),
            call('tests/data/3.jpg', 'tests/out/2017/summer/3.jpg'),
            call('tests/data/4.jpg', 'tests/out/2017/winter (end)/4.jpg'),
        ]
        print(patched_copy.call_args_list)
        patched_copy.assert_has_calls(calls, any_order=True)
