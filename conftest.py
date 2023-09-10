import pytest

from containers import Container


@pytest.fixture
def container():
    ioc = Container()
    yield ioc
