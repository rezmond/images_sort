import io
import contextlib
from unittest.mock import patch, call, Mock, MagicMock

import pytest

from core.entities.exceptions import NoArgumentPassedError
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
def view(container, controller_mock):
    with container.controller.override(controller_mock):
        view = container.view()

    yield view


def assert_argument_errors_contains(
        exc_info, std_err_file, *msg_containing_words):
    assert exc_info.value.code == 2

    printed_error = std_err_file.getvalue()
    for words in msg_containing_words:
        assert words in printed_error


@contextlib.contextmanager
def raises_argument_errors():
    std_err_file = io.StringIO()
    with contextlib.redirect_stderr(std_err_file), \
            pytest.raises(SystemExit) as exc_info:
        yield (exc_info, std_err_file)


def test_filled_params(view, controller_mock):

    with patch('sys.argv', [None, '/src/folder', '/dst/folder']):
        view.show()

    controller_mock.assert_has_calls([
        call.set_src_folder('/src/folder'),
        call.set_dst_folder('/dst/folder'),
    ])


def test_required_src_folder(view):
    with patch('sys.argv', [None]),\
            raises_argument_errors() as exc_data:
        view.show()

    assert_argument_errors_contains(*exc_data, 'src', 'required')


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

    src = '/src/path/test.jpeg'
    final_dst = '/dst/path/test_6.jpeg'

    file_way = FileWay(
        src=src,
        dst='/dst/path',
        full_dst=final_dst,
        type=MoveType.MEDIA
    )
    move_report = MoveReport(
        file_way=file_way,
        result=MoveResult.MOVED,
    )
    printed_list = view.file_moved_report_to_str(move_report)

    assert printed_list == f'\r\033[K{src} -> {final_dst}'
