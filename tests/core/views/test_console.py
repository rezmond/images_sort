# -*- coding: utf-8 -*-

from unittest.mock import patch, call

from ....core.views.console import ConsoleView


class TestConsole:

    def test_filled_params(self):
        with \
            patch('images_sort.core.model.model.MoverModel') as patched_model,\
            patch('images_sort.core.controllers.ConsoleViewController') \
                as patched_controller:
            view = ConsoleView(patched_controller(), patched_model())

        with patch('sys.argv', [None, '-i', '/src/folder', '-o', '/dst/folder']):
            view.show()

        patched_controller.assert_has_calls([
            call.set_src_folder('/src/folder'),
            call.set_dst_folder('/dst/folder'),
        ])

        patched_model.assert_has_calls([
            call.move(),
        ])
