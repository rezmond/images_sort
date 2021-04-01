from unittest.mock import Mock
from datetime import datetime

import pytest

from containers import Container


@pytest.fixture
def container():
    ioc = Container()
    yield ioc


def test_can_get_data_from_exif(container):
    exif_data_getter_mock = Mock(return_value='2000-01-01T12:00:00')
    with container.exif_data_getter.override(exif_data_getter_mock):
        instance = container.image_presenter()

    assert instance.get_date('') == datetime(2000, 1, 1, 12, 0, 0)


def test_can_get_data_from_exif_2(container):
    exif_data_getter_mock = Mock(return_value='2000:01:01 12:00:00.001')
    with container.exif_data_getter.override(exif_data_getter_mock):
        instance = container.image_presenter()

    assert instance.get_date('') == datetime(2000, 1, 1, 12, 0, 0)


def test_correct_none_handle(container):
    exif_data_getter_mock = Mock(return_value=None)
    with container.exif_data_getter.override(exif_data_getter_mock):
        instance = container.image_presenter()

    assert instance.get_date('') is None
