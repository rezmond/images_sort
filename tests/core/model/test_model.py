# -*- coding: utf-8 -*-

from unittest.mock import patch

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
