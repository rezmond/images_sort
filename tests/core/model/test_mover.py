# -*- coding: utf-8 -*-

from unittest.mock import patch, call, Mock

import pytest

from ....utils import full_path
from ....core.model.mover import Mover
from .fixtures import get_move_map


class TestMover:

    def test_init(self):
        attrs = {
            'scan.return_value': (get_move_map(), []),
        }
        scanner_mock = Mock(**attrs)
        mover = Mover(scanner_mock)
        with pytest.raises(ValueError) as exc_info:
            mover.move('test-1')

        assert 'absolute' in str(exc_info.value), \
            'Should catch not absolute the destination folder path'

        mover = Mover(scanner_mock)
        assert mover.move(full_path('test-1')), 'Should be silent'

    @patch('os.makedirs')
    def test_move(self, _not_used):
        mover = Mover(get_move_map())
        on_item_moved_handler_mock = Mock()
        mover.on_image_moved += on_item_moved_handler_mock

        with patch('shutil.copy2') as patched_copy:
            move_result = mover.move(full_path('tests/out'))

        calls = [
            call(
                full_path('tests/data/2.jpg'),
                full_path('tests/out/2017/spring/2_1.jpg')
            ),
            call(
                full_path('tests/data/3.jpg'),
                full_path('tests/out/2017/summer/3.jpg')
            ),
            call(
                full_path('tests/data/4.jpg'),
                full_path('tests/out/2017/winter (end)/4.jpg')
            ),
        ]
        patched_copy.assert_has_calls(calls, any_order=True)

        calls = [
            call(full_path('tests/out/2017/spring/2_1.jpg')),
            call(full_path('tests/out/2017/summer/3.jpg')),
            call(full_path('tests/out/2017/winter (end)/4.jpg')),
        ]
        on_item_moved_handler_mock\
            .assert_has_calls(calls, any_order=True)

        assert move_result == ([
            full_path('tests/data/1.jpg'),
        ], [
            full_path('tests/data/2.jpg'),
            full_path('tests/data/3.jpg'),
            full_path('tests/data/4.jpg')
        ]), 'Should return correct MoveResult'
