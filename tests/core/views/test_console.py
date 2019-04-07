# -*- coding: utf-8 -*-

from unittest.mock import patch

from ....core.views.console import ConsoleView


class TestConsole:

    def test_filled_params(self):
        with \
            patch('images_sort.core.model.model.MoverModel') as patched_model,\
            patch('images_sort.core.controllers.ConsoleViewController') \
                as patched_controller:
            view = ConsoleView(patched_controller(), patched_model())

        with patch('sys.argv', [None, '-i', 'src', '-o', 'dst']):
            view.show()
