from unittest.mock import Mock
from datetime import datetime


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


def test_getting_from_file_Nname(container):
    exif_data_getter_mock = Mock(return_value=None)
    with container.exif_data_getter.override(exif_data_getter_mock):
        instance = container.image_presenter()

    assert instance.get_date('20000429_123') == datetime(2000, 4, 29, 0, 0, 0)
    assert instance.get_date('20000429_456') == datetime(2000, 4, 29, 0, 0, 0)
    assert instance.get_date('20000529_456') == datetime(2000, 5, 29, 0, 0, 0)
    assert instance.get_date('20000529456') is None
    assert instance.get_date('20000431_123') is None
