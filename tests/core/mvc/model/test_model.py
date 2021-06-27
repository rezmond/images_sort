from unittest.mock import call, Mock

import pytest

from core.types import FileWay, MoveType, MoveReport, MoveResult
from core.entities.scanner.base import ScannerBase
from core.entities.mover import MoverBase
from core.mvc.model import OutputBoundary
from tests.utils import overrides

mover_mock = None
scanner_mock = None


@pytest.fixture
def get_model(container):
    def model_supplier(**mocks):
        global mover_mock
        global scanner_mock

        def map_mock(move):
            move('')

        scanner_mock = Mock(spec=ScannerBase, **{
            'scan.return_value': move_types
        })

        mover_mock = Mock(spec=MoverBase, **{
            'set_dst_folder.return_value': Mock(
                **{'either.return_value': Mock(map=map_mock)}),
            'move.return_value': Mock(
                spec=MoveReport,
                result=MoveResult.MOVED
            ),
        })

        with overrides(
            container,
            scanner=scanner_mock,
            mover=mover_mock,
            **mocks
        ):
            model = container.model()

        return model

    yield model_supplier


def scan(model, src):
    def on_move_started(move_gen, length):
        list(move_gen)

    output_boundary_mock = Mock(
        spec=OutputBoundary, on_move_started=on_move_started)

    model.set_output_boundary(output_boundary_mock)

    model.set_src_folder(src)
    model.scan()


def move(model, dst):
    model.set_dst_folder(dst)
    model.move()


def assert_moved(dst, is_clean_mode):
    mover_mock.set_dst_folder.assert_called_once_with(dst)
    mover_mock.move.assert_has_calls([
        call(x, is_clean_mode) for x in move_types
    ])


move_types = [FileWay(src=str(x), type=MoveType.MEDIA) for x in range(3)]


def test_safe_move(get_model):
    model = get_model()

    scan(model, 'src')
    scanner_mock.scan.assert_called_once_with('src')

    move(model, 'dst')
    assert_moved('dst', False)


def test_danger_move(get_model):
    model = get_model()

    scan(model, 'src')
    scanner_mock.scan.assert_called_once_with('src')

    model.clean_mode(True)

    move(model, 'dst')
    assert_moved('dst', True)
