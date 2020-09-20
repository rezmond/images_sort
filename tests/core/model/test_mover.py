# -*- coding: utf-8 -*-

from unittest.mock import patch, call, Mock

import pytest

from ....utils import full_path
from ....core.model.mover import Mover
from ....core.model.scanner import Scanner
from ....core.model.types import ScanResult
from ...utils import create_ioc
from .fixtures import get_move_map


class TestMover:

    def test_move_without_dst_param(self):
        ioc = create_ioc()
        mover = Mover(ioc)
        with pytest.raises(ValueError) as exc_info:
            mover.move(ScanResult(None, None, None), None)

        assert 'path did not set' in str(exc_info.value), \
            'Should catch not set the src or the dst folder path'

    def test_move_by_relative_path(self):
        ioc = create_ioc()
        mover = Mover(ioc)
        with pytest.raises(ValueError) as exc_info:
            mover.move(ScanResult(None, None, None), 'test-1')

        assert 'absolute' in str(exc_info.value), \
            'Should catch not absolute the destination folder path'

    @patch.object(Scanner, 'scan', return_value=(get_move_map(), [], []))
    def test_move_by_absolute_path(self, patched_scanner):
        ioc = create_ioc()
        ioc.add('compare', lambda x, _: x.endswith('1.jpg'))
        mover = Mover(ioc)
        on_item_moved_handler_mock = Mock()
        mover.on_image_moved += on_item_moved_handler_mock

        move_result = mover.move(
            ScanResult({
                '2017': {
                    'spring': [{'path': full_path('tests/data/2.jpg')}],
                    'summer': [{'path': full_path('tests/data/3.jpg')}],
                    'winter (end)': [{
                        'path': full_path('tests/data/5.jpg')
                    }, {
                        'path': full_path('tests/data/4.jpg')
                    }],
                    'winter (begin)': [{
                        'path': full_path('tests/data/1.jpg')
                    }],
                    'summer': [{'path': full_path('tests/data/3.jpg')}],
                }
            }, [], []), full_path('tests/out'))

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

        copy_mock = ioc.get('copy')
        copy_mock.assert_has_calls(calls, any_order=True)

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
        ], [], []), 'Should return correct MoveResult'
