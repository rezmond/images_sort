from unittest.mock import Mock

import pytest

from containers import Container
from core.model import MoverModel
from core.views import ConsoleView


@pytest.fixture
def model():
    yield Mock(spec=MoverModel)


@pytest.fixture
def view_class():
    yield Mock(spec=ConsoleView)


@pytest.fixture
def container(model, view_class):
    ioc = Container()
    with ioc.model.override(model),\
            ioc.view_class.override(view_class):
        yield ioc


def test_set_params(model, view_class, container):
    controller = container.controller()
    controller.set_src_folder('/test/src/path')
    controller.set_dst_folder('/test/dst/path')

    view_class.return_value.show.assert_called_once()
    model.set_src_folder.assert_called_once_with('/test/src/path')
    model.set_dst_folder.assert_called_once_with('/test/dst/path')


def test_move(model, view_class, container):
    controller = container.controller()
    controller.move()
    model.move.assert_called_once()


def test_enable_moved_images_log(model, view_class, container):
    controller = container.controller()
    iadd_mock = Mock()
    model.on_image_moved.__iadd__ = iadd_mock
    controller.enable_moved_images_log()
    iadd_mock.assert_called_once()


def test_handle_image_moved(model, view_class, container):
    def mock_of_handler(handler):
        handler(('a', 'b'))

    controller = container.controller()
    model.on_image_moved.__iadd__ = Mock(side_effect=mock_of_handler)
    controller.enable_moved_images_log()

    view_class.return_value.handle_image_moved\
        .assert_called_once_with(('a', 'b'))
