from datetime import date

import pytest


@pytest.fixture
def move_map(container):
    yield container.move_map()


def test_correct_add_data(move_map):
    test_data = {'test': 'object'}
    move_map.add_data(date.fromisoformat('2020-01-01'), test_data)

    assert move_map.get_map() == {
        '2020': {
            'winter (begin)': [test_data]
        }
    }

    test_data_2 = {'test': 'object2'}
    move_map.add_data(date.fromisoformat('2020-01-01'), test_data_2)

    assert move_map.get_map() == {
        '2020': {
            'winter (begin)': [test_data, test_data_2]
        }
    }

    test_data_3 = {'test': 'object2'}
    move_map.add_data(date.fromisoformat('2020-04-01'), test_data_3)

    assert move_map.get_map() == {
        '2020': {
            'winter (begin)': [test_data, test_data_3],
            'spring': [test_data_3],
        }
    }
