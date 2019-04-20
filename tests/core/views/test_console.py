# -*- coding: utf-8 -*-

import io
import contextlib
from unittest import TestCase
from unittest.mock import patch, call

import pytest

from ....core.views.console import ConsoleView


class TestConsole(TestCase):

    def setUp(self):
        with \
            patch('images_sort.core.model.model.MoverModel') as patched_model,\
            patch('images_sort.core.controllers.ConsoleViewController') \
                as patched_controller:
            self._patched_controller = patched_controller()
            self._patched_model = patched_model()
            self._view = ConsoleView(
                self._patched_controller,
                self._patched_model,
            )

    def test_filled_params(self):

        with patch('sys.argv', [None, '-i', '/src/folder', '-o', '/dst/folder']):
            self._view.show()

        self._patched_controller.assert_has_calls([
            call.set_src_folder('/src/folder'),
            call.set_dst_folder('/dst/folder'),
        ])

        self._patched_model.assert_has_calls([
            call.move(),
        ])

    def test_help_param(self):
        file_ = io.StringIO()
        with contextlib.redirect_stdout(file_),\
                pytest.raises(SystemExit) as exc_info,\
                patch('sys.argv', [None, '-h']):
            self._view.show()

        assert exc_info.value.code == 0, 'Incorrect exit status'

        assert (not self._patched_controller.mock_calls) \
            and (not self._patched_model.mock_calls), \
            'Nothing should be called when the help instruction was calling'

        printed_help = file_.getvalue()
        for x in (' -i ', ' -o '):
            assert x in printed_help, 'Incorrect printed the help message'
