# -*- coding: utf-8 -*-

from unittest.mock import patch
from ...core.start import main


class TestStart:

    def test_command_with_incorrect_params(self):
        with patch(
            'images_sort.core.start.ConsoleViewController',
        ) as patched_controller:
            main()

        instance = patched_controller.return_value
        instance.move.assert_called_once()
