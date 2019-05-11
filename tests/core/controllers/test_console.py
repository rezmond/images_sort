# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock


from ....core.model import MoverModel
from ....core.controllers.console import ConsoleViewController


@patch.object(ConsoleViewController, 'view_class', return_value=Mock())
class TestConsole:

    def test_set_params(self, patched_controller_view):
        model = Mock(spec=MoverModel)
        controller = ConsoleViewController(model)

        controller.set_src_folder('/test/src/path')
        controller.set_dst_folder('/test/dst/path')

        patched_controller_view.return_value.show.assert_called_once()
        model.set_src_folder.assert_called_once_with('/test/src/path')
        model.set_dst_folder.assert_called_once_with('/test/dst/path')

    def test_move(self, patched_controller_view):
        model = Mock(spec=MoverModel)
        controller = ConsoleViewController(model)

        controller.move()
        model.move.assert_called_once()
