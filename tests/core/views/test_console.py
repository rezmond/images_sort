# -*- coding: utf-8 -*-

import io
import contextlib
from unittest import TestCase
from unittest.mock import patch, call, Mock

import pytest

from ....core.views.console import ConsoleView
from ....core.utils import MoveResult


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

        with patch('sys.argv', [None, '/src/folder', '/dst/folder']):
            self._view.show()

        self._patched_controller.assert_has_calls([
            call.set_src_folder('/src/folder'),
            call.set_dst_folder('/dst/folder'),
        ])

    def test_param_list_items_true(self):

        with patch('sys.argv', [None, '-l', '/src/folder', '/dst/folder']):
            self._view.show()

        self._patched_controller.enable_moved_images_log\
            .assert_called_once_with(True)

    def test_param_list_items_false(self):
        with patch('sys.argv', [None, '/src/folder', '/dst/folder']):
            self._view.show()

        self._patched_controller.enable_moved_images_log\
            .assert_called_once_with(False)

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
        for x in (' src ', ' dst '):
            assert x in printed_help, 'Incorrect printed the help message'

    def test_incorrect_param(self):
        file_ = io.StringIO()
        with contextlib.redirect_stderr(file_),\
                pytest.raises(SystemExit) as exc_info,\
                patch('sys.argv', [None, '--incorrect-parameter']):
            self._view.show()
        assert exc_info.value.code == 2, 'Incorrect exit status'

        assert (not self._patched_controller.mock_calls) \
            and (not self._patched_model.mock_calls), \
            'Nothing should be called when the help instruction was calling'

        printed_help = file_.getvalue()
        assert str(printed_help).startswith('usage')

    def test_show_list_of_moved(self):
        file_ = io.StringIO()
        with contextlib.redirect_stdout(file_),\
                patch('sys.argv', [None, '/src/folder', '/dst/folder', '-l']):
            self._view.handle_image_moved(('test-src', 'test-dst'))
        printed_list = file_.getvalue()

        assert 'test-src' in printed_list, \
            'Not showed just moved image src path'
        assert 'test-dst' in printed_list, \
            'Not showed just moved image dst path'

    def test_show_report(self):
        file_ = io.StringIO()

        def mock_of_handler(handler):
            handler(MoveResult([], [1], [2, 2], [3, 3, 3]))

        self._patched_model.on_move_finished.__iadd__ = Mock(
            side_effect=mock_of_handler)
        with contextlib.redirect_stdout(file_),\
                patch('sys.argv', [None, '/src/folder', '/dst/folder', '-l']):
            self._view.show()
        printed_list = file_.getvalue()

        for i in range(4):
            assert str(i) in printed_list, 'Incorrect move report'
