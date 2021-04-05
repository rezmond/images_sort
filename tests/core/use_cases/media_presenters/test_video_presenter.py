from datetime import datetime

import pytest


@pytest.fixture
def video_presenter(container):
    yield container.video_presenter()


def test_can_get_data_from_file_name(video_presenter):
    assert video_presenter.get_date(
        '/test/path/20000101_120000.mp4') == datetime(2000, 1, 1, 12, 0, 0)


def test_correct_none_handle(video_presenter):
    assert video_presenter.get_date('') is None


def test_correct_returns_extensions(video_presenter):
    assert video_presenter.get_extensions() == ('.mp4', )
