# -*- coding: utf-8 -*-

import pytest

from ...core.start import main


class TestStart:

    def test_command_with_not_correct_params(self):
        with pytest.raises(ValueError) as exc_info:
            main('test')

        assert str(exc_info.value) == 'The source folder was not passed', \
            'Should raise exception with correct message'
