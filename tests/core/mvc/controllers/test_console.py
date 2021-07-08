from unittest.mock import Mock, call

import pytest

from core.mvc.model import MoverModel
from core.mvc.views import ConsoleView


@pytest.fixture
def model():
    yield Mock(spec=MoverModel)


@pytest.fixture
def controller(container, model):
    console_view = Mock(spec=ConsoleView)

    with container.model.override(model):
        instance = container.controller()

    instance.set_io_interactor(console_view)
    return instance


def test_set_params(controller, model):
    controller.set_src_folder('/test/src/path')
    controller.set_dst_folder('/test/dst/path')

    model.set_src_folder.assert_called_once_with('/test/src/path')
    model.set_dst_folder.assert_called_once_with('/test/dst/path')


def test_move_mode(controller, model):
    controller.move_mode(True)
    model.move_mode.assert_called_once_with(True)


def test_clean_mode_is_passing_value_down(controller, model):
    controller.clean_mode(True)
    controller.clean_mode(False)
    model.clean_mode.assert_has_calls([
        call(True),
        call(False),
    ])
