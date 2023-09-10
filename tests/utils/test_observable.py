from unittest.mock import Mock

from src.utils import Observable


def test_observable():
    mocked_hanlder_1 = Mock()
    mocked_hanlder_2 = Mock()
    instance = Observable()
    instance += mocked_hanlder_1
    instance += mocked_hanlder_2

    instance.update('test-token')

    mocked_hanlder_1.assert_called_once_with('test-token')
    mocked_hanlder_2.assert_called_once_with('test-token')
