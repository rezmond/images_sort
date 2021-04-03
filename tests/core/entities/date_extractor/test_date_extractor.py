from unittest.mock import Mock
from datetime import datetime

import pytest

from containers import Container
from core.entities import MediaPresenterBase


@pytest.fixture
def container():
    ioc = Container()
    yield ioc


def create_media_mock(*extensions):
    media_mock = Mock(spec=MediaPresenterBase)
    media_mock.get_extensions = Mock(return_value=extensions)
    media_mock.get_date = Mock(spec=datetime.date)
    return media_mock


@pytest.fixture
def extractor_pack_single(container):
    media_mock = create_media_mock('.a', '.b')
    with container.media_presenters.override([media_mock]):
        instance = container.date_extractor()

    yield instance, media_mock


@pytest.fixture
def extractor_pack_multiple(container):
    media_mock_1 = create_media_mock('.a', '.b')
    media_mock_2 = create_media_mock('.c', '.d')
    with container.media_presenters.override((media_mock_1, media_mock_2)):
        instance = container.date_extractor()

    yield instance, (media_mock_1, media_mock_2)


def test_allowed_extensions_of_singe(extractor_pack_single):
    date_extractor, _ = extractor_pack_single
    assert date_extractor.is_allowed_extension('test/path/foo.a')
    assert not date_extractor.is_allowed_extension('test/path/foo.c')


def test_get_date_of_single(extractor_pack_single):
    date_extractor, media_mock = extractor_pack_single

    assert date_extractor.get_date('test/path/foo.c') is None
    assert date_extractor.get_date('test/path/foo.a')

    media_mock.get_date.assert_called_with('test/path/foo.a')


def test_allowed_extensions_of_multimple(extractor_pack_multiple):
    date_extractor, _ = extractor_pack_multiple
    assert date_extractor.is_allowed_extension('test/path/foo.a')
    assert date_extractor.is_allowed_extension('test/path/foo.d')
    assert not date_extractor.is_allowed_extension('test/path/foo.f')


def test_get_date_of_multimple(extractor_pack_multiple):
    date_extractor, media_mocks = extractor_pack_multiple

    assert date_extractor.get_date('test/path/foo.f') is None
    assert date_extractor.get_date('test/path/foo.a')
    assert date_extractor.get_date('test/path/foo.d')

    media_mocks[0].get_date.assert_called_with('test/path/foo.a')
    media_mocks[1].get_date.assert_called_with('test/path/foo.d')
