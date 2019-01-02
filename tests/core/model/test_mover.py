# -*- coding: utf-8 -*-

import os
from unittest.mock import patch, call, Mock, PropertyMock

import pytest

from ....utils import full_path
from ....core.model.mover import Mover
from .fixtures import get_move_map


class TestMover:

    @patch('os.makedirs')
    def test_move(self, _not_used, ):
        attrs = {
            'scan.return_value': (get_move_map(), []),
        }
        scanner_mock = Mock(**attrs)
        type(scanner_mock).dst_folder = PropertyMock(
            return_value=full_path('tests/out'))
        mover = Mover(scanner_mock)

        with patch('shutil.copy2') as patched_copy:
            move_result = mover.move()

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

        assert move_result == ([
            full_path('tests/data/1.jpg'),
        ], [
            full_path('tests/data/2.jpg'),
            full_path('tests/data/3.jpg'),
            full_path('tests/data/4.jpg')
        ]), 'Should return correct MoveResult'
