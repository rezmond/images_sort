from unittest.mock import Mock


def get_progressbar_mock(expected_length):
    moved = []

    def progressbar_mock(gen, length, **kwargs):
        assert length == expected_length

        moved.extend(map(kwargs['item_show_func'], gen))
        mock = Mock()
        mock.__enter__ = Mock(return_value=moved)
        mock.__exit__ = Mock(return_value=False)

        return mock

    progressbar_mock.moved = moved
    return progressbar_mock
