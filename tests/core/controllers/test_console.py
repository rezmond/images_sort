# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock


from ....core.model import MoverModel
from ....core.controllers.console import ConsoleViewController
from ....core.views.console import ConsoleView


class TestConsole:

    def test_set_params(self):
        model = Mock(spec=MoverModel)
        with patch.object(ConsoleView, 'show') as patched_controller_show:
            controller = ConsoleViewController(model)

        controller.set_src_folder('/test/src/path')
        controller.set_dst_folder('/test/dst/path')

        patched_controller_show.assert_called_once()
        model.set_src_folder.assert_called_once_with('/test/src/path')
        model.set_dst_folder.assert_called_once_with('/test/dst/path')

    def test_move(self):
        model = Mock(spec=MoverModel)
        with patch.object(ConsoleView, 'show'):
            controller = ConsoleViewController(model)

        controller.move()
        model.move.assert_called_once()
