from unittest.mock import Mock, call

import pytest

from core.model import MoverModel
from core.views import ConsoleView


@pytest.fixture
def model():
    yield Mock(spec=MoverModel)


@pytest.fixture
def view_class():
    yield Mock(spec=ConsoleView)


@pytest.fixture
def controller(container, model, view_class):
    with container.model.override(model),\
            container.view_class.override(view_class):
        instance = container.controller()
    return instance


def test_set_params(controller, model, view_class):
    controller.set_src_folder('/test/src/path')
    controller.set_dst_folder('/test/dst/path')

    view_class.return_value.show.assert_called_once()
    model.set_src_folder.assert_called_once_with('/test/src/path')
    model.set_dst_folder.assert_called_once_with('/test/dst/path')


def test_move(controller, model, view_class):
    controller.move()
    model.move.assert_called_once()


def test_enable_moved_images_log(controller, model, view_class):
    iadd_mock = Mock()
    model.on_move_finished.__iadd__ = iadd_mock
    controller.enable_moved_images_log()
    iadd_mock.assert_called_once()


def test_handle_image_moved(controller, model, view_class):
    def received_handler(*args):
        return None

    def mock_of_handler(_, handler):
        nonlocal received_handler
        received_handler = handler

    model.on_move_finished.__iadd__ = mock_of_handler
    controller.enable_moved_images_log()
    received_handler(('a', 'b'))

    view_class.return_value.handle_move_finished\
        .assert_called_once_with(('a', 'b'))


def test_clean_mode_is_passing_value_down(controller, model, view_class):
    controller.clean_mode(True)
    controller.clean_mode(False)
    model.clean_mode.assert_has_calls([
        call(True),
        call(False),
    ])
