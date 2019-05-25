# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock

from ....core.model.model import MoverModel
from ....core.model.mover import Mover


class TestModel:

    def test_move_call(self):
        model = MoverModel()
        model.set_dst_folder('dst')
        model.set_src_folder('src')
        with patch.object(Mover, 'move') as patched_move:
            model.move()

        patched_move.assert_called_with('src', 'dst')

    def test_on_image_move_prop(self):
        model = MoverModel()
        with patch.object(Mover, 'on_image_moved') as patched_prop:
            patched_prop.__get__ = Mock(return_value='')
            patched_prop.__get__.assert_not_called()
            model.on_image_moved
            patched_prop.__get__.assert_called_once()

    def test_on_move_finish_report_subscribe(self):
        iadd_mock = Mock()
        with patch('images_sort.core.model.mover.Observable') as patched_observable:
            patched_observable.__iadd__ = iadd_mock
            model = MoverModel()
            model.on_move_finished += Mock()
        patched_observable.return_value.__iadd__.assert_called_once()
