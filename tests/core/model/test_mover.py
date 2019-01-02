# -*- coding: utf-8 -*-

import os
from unittest.mock import patch, call, Mock, PropertyMock

import pytest

from ....core.model.mover import Mover
from .fixtures import get_move_map

ROOT_DIR = os.path.abspath(__file__ + '../../../../../')


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
            call(os.path.join(ROOT_DIR, 'tests/data/2.jpg'),
                 'tests/out/2017/spring/2.jpg'),
            call(os.path.join(ROOT_DIR, 'tests/data/3.jpg'),
                 'tests/out/2017/summer/3.jpg'),
            call(os.path.join(ROOT_DIR, 'tests/data/4.jpg'),
                 'tests/out/2017/winter (end)/4.jpg'),
        ]
        patched_copy.assert_has_calls(calls, any_order=True)

        assert move_result == ([
            os.path.join(ROOT_DIR, 'tests/data/1.jpg'),
        ], [
            os.path.join(ROOT_DIR, 'tests/data/2.jpg'),
            os.path.join(ROOT_DIR, 'tests/data/3.jpg'),
            os.path.join(ROOT_DIR, 'tests/data/4.jpg')
        ]), 'Should return correct MoveResult'
