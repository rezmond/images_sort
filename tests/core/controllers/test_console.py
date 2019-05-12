# -*- coding: utf-8 -*-

from unittest.mock import patch, Mock
from unittest import TestCase

from ....core.model import MoverModel
from ....core.controllers.console import ConsoleViewController


class TestConsole(TestCase):

    def setUp(self):
        patcher = patch.object(
            ConsoleViewController, 'view_class', return_value=Mock())
        self._patched_controller_view = patcher.start()
        self._model = Mock(spec=MoverModel)
        self._controller = ConsoleViewController(self._model)

    def test_set_params(self):
        self._controller.set_src_folder('/test/src/path')
        self._controller.set_dst_folder('/test/dst/path')

        self._patched_controller_view.return_value.show.assert_called_once()
        self._model.set_src_folder.assert_called_once_with('/test/src/path')
        self._model.set_dst_folder.assert_called_once_with('/test/dst/path')

    def test_move(self):
        self._controller.move()
        self._model.move.assert_called_once()
