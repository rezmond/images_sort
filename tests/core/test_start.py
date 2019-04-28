# -*- coding: utf-8 -*-

import pytest

from unittest.mock import patch
from ...core.start import main


class TestStart:

    def test_command_with_incorrect_params(self):
        argv_data = [None]
        with pytest.raises(ValueError) as exc_info, \
                patch('sys.argv', argv_data):
            main()

        assert str(exc_info.value)\
            .startswith('The source folder\'s path did not set'), \
            'Should raise exception with correct message'
