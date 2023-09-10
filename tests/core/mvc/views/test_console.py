import io
import contextlib
from unittest.mock import patch, call, Mock, MagicMock, mock_open

import pytest

from src.mvc.controllers import ControllerBase
from src.mvc.model import MoverModel
from src.types import MoveReport, FileWay, MoveType, MoveResult, TotalMoveReport
from tests.utils import get_progressbar_mock


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


def test_required_dst_folder(view):
    '''
    The dst argument might be unnecessary during scan only mode
    '''
    with patch('sys.argv', [None, '/src/folder']),\
            raises_argument_errors() as exc_data:
        view.show()

    assert_argument_errors_contains(*exc_data, 'dst', 'required')


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
    def assert_app_logic_not_called():
        assert not controller_mock.mock_calls
        assert not model_mock.mock_calls

    with raises_argument_errors() as exc_data,\
            patch('sys.argv', [None, '--incorrect-parameter']):
        view.show()

    assert_argument_errors_contains(*exc_data, 'usage')
    assert_app_logic_not_called()


def test_show_report(view, model_mock):
    caught_io = io.StringIO()
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

    progressbar_mock = get_progressbar_mock(1)

    with patch('click.progressbar', progressbar_mock), \
            contextlib.redirect_stdout(caught_io):
        view.show_moving_progress(
            (move_report,),
            length=1,
            should_report_be_shown=True,
        )

    assert caught_io.getvalue() == f'\n\n\033[K{src} --> {final_dst}\033[2A\n'


def test_report_file_name(view, model_mock):
    caught_io = io.StringIO()
    is_exists_check_attempts_count = 0
    expected_attempts = 3

    def is_exists_mock(file_path):
        nonlocal is_exists_check_attempts_count
        is_exists_check_attempts_count += 1
        return is_exists_check_attempts_count < expected_attempts

    mock_of_open = mock_open()

    with contextlib.redirect_stdout(caught_io),\
        patch('os.path.exists', is_exists_mock), \
        patch(
        'src.mvc.views.console.console.open', mock_of_open
    ):
        view.show_total_move_report(
            TotalMoveReport(), log_to_folder="/dst/path")

    assert mock_of_open.mock_calls[0] == call(
        f'/dst/path/report-{expected_attempts - 1}.txt', 'w'
    )
