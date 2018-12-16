# -*- coding: utf-8 -*-

import pytest

from ...core.start import main


class TestStart:

    def test_command_without_params(self):
        with pytest.raises(ValueError) as exc_info:
            main('test')

        assert str(exc_info.value) == 'Не задана папка источник', \
            'Should raise exception with correct message'
