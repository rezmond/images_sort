from datetime import date

import pytest


@pytest.fixture
def move_map(container):
    yield container.move_map()


def test_correct_result(move_map):
    dst_path = move_map.get_dst_path(date.fromisoformat('2020-01-01'))
    assert dst_path == '2020/winter (begin)'

    dst_path = move_map.get_dst_path(date.fromisoformat('2020-04-01'))
    assert dst_path == '2020/spring'
