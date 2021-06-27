from unittest.mock import call, Mock

from core.types import FileWay, MoveType, MoveReport, MoveResult
from core.entities.scanner.base import ScannerBase
from core.entities.mover import MoverBase
from core.mvc.model import OutputBoundary
from tests.utils import overrides


def get_model(container, **mocks):
    with overrides(container, **mocks):
        model = container.model()

    return model


def test_move_call(container):

    move_types = [FileWay(src=str(x), type=MoveType.MEDIA) for x in range(3)]

    def map_mock(move):
        move('')

    def on_move_started(move_gen, length):
        list(move_gen)

    scanner_mock = Mock(spec=ScannerBase, **{
        'scan.return_value': move_types
    })

    mover_mock = Mock(spec=MoverBase, **{
        'set_dst_folder.return_value': Mock(
            **{'either.return_value': Mock(map=map_mock)}),
        'move.return_value': Mock(spec=MoveReport, result=MoveResult.MOVED),
    })

    def assert_moved():
        is_clean_mode = False
        mover_mock.move.assert_has_calls([
            call(x, is_clean_mode) for x in move_types
        ])

    output_boundary_mock = Mock(
        spec=OutputBoundary, on_move_started=on_move_started)

    model = get_model(
        container,
        scanner=scanner_mock,
        mover=mover_mock,
    )

    model.set_output_boundary(output_boundary_mock)

    model.set_src_folder('src')
    model.scan()

    scanner_mock.scan.assert_called_once_with('src')

    model.set_dst_folder('dst')
    model.move()

    mover_mock.set_dst_folder.assert_called_once_with('dst')
    assert_moved()


def test_clean_mode_safe(container):
    scanner_mock = Mock(spec=ScannerBase, **{'scan.return_value': [None]})
    mover_mock = Mock(spec=MoverBase)
    with container.mover.override(mover_mock),\
            container.scanner.override(scanner_mock):
        model = container.model()
    model.move()

    mover_mock.move.assert_called_once_with(None, None, False)


def test_clean_mode_dangerously(container):
    scanner_mock = Mock(spec=ScannerBase, **{'scan.return_value': [None]})
    mover_mock = Mock(spec=MoverBase)
    with container.mover.override(mover_mock),\
            container.scanner.override(scanner_mock):
        model = container.model()
    model.clean_mode(True)
    model.move()

    mover_mock.move.assert_called_once_with(None, None, True)
