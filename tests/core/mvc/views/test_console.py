import io
import contextlib
from unittest.mock import patch, call, Mock, MagicMock

import pytest

from core.mvc.controllers import ControllerBase
from core.mvc.model import MoverModel
from core.types import MoveReport, FileWay, MoveType, MoveResult


@pytest.fixture
def model_mock():
    yield MagicMock(spec=MoverModel)


@pytest.fixture
def controller_mock():
    yield Mock(spec=ControllerBase)


@pytest.fixture
def view(container, model_mock, controller_mock):
    view_class = container.view_class()
    yield view_class(controller_mock, model_mock)


def test_filled_params(view, controller_mock):

    with patch('sys.argv', [None, '/src/folder', '/dst/folder']):
        view.show()

    controller_mock.assert_has_calls([
        call.set_src_folder('/src/folder'),
        call.set_dst_folder('/dst/folder'),
    ])


def test_param_list_items_true(view, controller_mock):

    with patch('sys.argv', [None, '-l', '/src/folder', '/dst/folder']):
        view.show()

    controller_mock.enable_moved_images_log\
        .assert_called_once_with(True)


def test_param_list_items_false(view, controller_mock):
    with patch('sys.argv', [None, '/src/folder', '/dst/folder']):
        view.show()

    controller_mock.enable_moved_images_log\
        .assert_called_once_with(False)


def test_help_param(view, controller_mock, model_mock):
    file_ = io.StringIO()
    with contextlib.redirect_stdout(file_),\
            pytest.raises(SystemExit) as exc_info,\
            patch('sys.argv', [None, '-h']):
        view.show()

    assert exc_info.value.code == 0, 'Incorrect exit status'

    assert (not controller_mock.mock_calls) \
        and (not model_mock.mock_calls), \
        'Nothing should be called when the help instruction was calling'

    printed_help = file_.getvalue()
    for x in (' src ', ' dst '):
        assert x in printed_help, 'Incorrect printed the help message'


def test_incorrect_param(view, controller_mock, model_mock):
    file_ = io.StringIO()
    with contextlib.redirect_stderr(file_),\
            pytest.raises(SystemExit) as exc_info,\
            patch('sys.argv', [None, '--incorrect-parameter']):
        view.show()
    assert exc_info.value.code == 2, 'Incorrect exit status'

    assert (not controller_mock.mock_calls) \
        and (not model_mock.mock_calls), \
        'Nothing should be called when the help instruction was calling'

    printed_help = file_.getvalue()
    assert str(printed_help).startswith('usage')


def test_show_report(view, model_mock):
    caught_io = io.StringIO()

    src = '/src/path/test.jpeg'
    final_dst = '/dst/path/test_6.jpeg'

    with contextlib.redirect_stdout(caught_io):
        view.handle_move_finished(MoveReport(
            file_way=FileWay(
                src=src,
                dst='/dst/path',
                full_dst=final_dst,
                type=MoveType.MEDIA
            ),
            result=MoveResult.MOVED,
        ))

    printed_list = caught_io.getvalue()

    assert printed_list == f'\r\033[K{src} -> {final_dst}'
