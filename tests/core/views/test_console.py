# -*- coding: utf-8 -*-
import sys

from unittest.mock import patch, call, Mock

from ....core.controllers import ConsoleViewController
from ....core.views.console import ConsoleView


class TestConsole:

    def test_filled_params(self):
        with patch('images_sort.core.model.model.MoverModel') as patched_model,\
                patch('images_sort.core.controllers.ConsoleViewController') as patched_controller:
            view = ConsoleView(patched_controller(), patched_model())

        argv_data = [None, '-i', 'src', '-o', 'dst']
        with patch('sys.argv', argv_data):
            view.show()
