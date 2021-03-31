from unittest import skip
from unittest.mock import Mock
from datetime import datetime

import pytest

from containers import Container
from core.entities import MediaPresenterBase


@pytest.fixture
def container():
    ioc = Container()
    yield ioc


@pytest.fixture
def extractor_pack(container):
    media_mock = Mock(spec=MediaPresenterBase)
    media_mock.get_extensions = Mock(return_value=['.a', '.b'])
    media_mock.get_date = Mock(spec=datetime.date)
    with container.media_presenters.override([media_mock]):
        instance = container.date_extractor()

    yield instance, media_mock


def test_allowed_extensions_of_singe(extractor_pack):
    date_extractor, media_mock = extractor_pack
    assert date_extractor.is_allowed_extension('test/path/foo.a')
    assert not date_extractor.is_allowed_extension('test/path/foo.c')


def test_get_date_of_single(extractor_pack):
    date_extractor, media_mock = extractor_pack

    assert date_extractor.get_date('test/path/foo.c') is None
    assert date_extractor.get_date('test/path/foo.a')

    media_mock.get_date.assert_called_with('test/path/foo.a')


@skip('to be implemented')
def test_allowed_extensions_of_multimple(extractor_pack):
    pass


@skip('to be implemented')
def test_get_date_of_multimple(extractor_pack):
    pass
