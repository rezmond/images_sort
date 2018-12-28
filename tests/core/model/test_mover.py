# -*- coding: utf-8 -*-

from unittest.mock import patch, call, Mock, PropertyMock

import pytest

from ....core.model.mover import Mover
from .fixtures import get_move_map


class TestMover:

    @patch('os.makedirs')
    def test_move(self, _not_used, ):
        attrs = {
            'scan.return_value': (get_move_map(), []),
        }
        scanner_mock = Mock(**attrs)
        type(scanner_mock).dst_folder = PropertyMock(return_value='tests/out')
        mover = Mover(scanner_mock)

        with patch('shutil.copy2') as patched_copy:
            move_result = mover.move()

        calls = [
            call('tests/data/1.jpg', 'tests/out/2017/winter (begin)/1.jpg'),
            call('tests/data/2.jpg', 'tests/out/2017/spring/2.jpg'),
            call('tests/data/3.jpg', 'tests/out/2017/summer/3.jpg'),
            call('tests/data/4.jpg', 'tests/out/2017/winter (end)/4.jpg'),
        ]
        patched_copy.assert_has_calls(calls, any_order=True)

        assert move_result == ([], [
            'tests/data/2.jpg',
            'tests/data/1.jpg',
            'tests/data/3.jpg',
            'tests/data/4.jpg'
        ]), 'Should return correct MoveResult'
