# -*- coding: utf-8 -*-

from unittest.mock import patch, call, Mock

import pytest

from ....utils import full_path
from ....core.model.mover import Mover
from ....core.model.scanner import Scanner
from .fixtures import get_move_map


class TestMover:

    def test_move_by_without_a_param(self):
        mover = Mover()
        with pytest.raises(ValueError) as exc_info:
            mover.move('/src_folder', None)

        assert 'path did not set' in str(exc_info.value), \
            'Should catch not set the src or the dst folder path'

    def test_move_by_relative_path(self):
        mover = Mover()
        with pytest.raises(ValueError) as exc_info:
            mover.move('/src_folder', 'test-1')

        assert 'absolute' in str(exc_info.value), \
            'Should catch not absolute the destination folder path'

    @patch('os.makedirs')
    @patch.object(Scanner, 'scan', return_value=(get_move_map(), []))
    def test_move_by_absolute_path(self, patched_scanner, _not_used):

        mover = Mover()
        on_item_moved_handler_mock = Mock()
        mover.on_image_moved += on_item_moved_handler_mock

        with patch('shutil.copy2') as patched_copy:
            move_result = mover.move('/src_folder', full_path('tests/out'))

        calls = [
            call(
                full_path('tests/data/2.jpg'),
                full_path('tests/out/2017/spring/2_1.jpg')
            ),
            call(
                full_path('tests/data/5.jpg'),
                full_path('tests/out/2017/winter (end)/5.jpg')
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
            call((
                full_path('tests/data/2.jpg'),
                full_path('tests/out/2017/spring/2_1.jpg')
            )),
            call((
                full_path('tests/data/3.jpg'),
                full_path('tests/out/2017/summer/3.jpg')
            )),
            call((
                full_path('tests/data/5.jpg'),
                full_path('tests/out/2017/winter (end)/5.jpg')
            )),
            call((
                full_path('tests/data/4.jpg'),
                full_path('tests/out/2017/winter (end)/4.jpg')
            )),
        ]
        on_item_moved_handler_mock\
            .assert_has_calls(calls, any_order=True)

        assert move_result == ([
            full_path('tests/data/2.jpg'),
            full_path('tests/data/3.jpg'),
            full_path('tests/data/5.jpg'),
            full_path('tests/data/4.jpg'),
        ], [
            full_path('tests/data/1.jpg'),
        ], []), 'Should return correct MoveResult'
