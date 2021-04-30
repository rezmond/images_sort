import contextlib
from unittest.mock import call, Mock, MagicMock, PropertyMock

import pytest

from core.entities.fs import FsManipulatorBase
from core.entities.scanner.base import ScannerBase
from core.entities.mover import MoverBase
from core.types import ScanResult
from core.utils.base import Observable
from ...fixtures import get_move_map


scanner_result = ScanResult(get_move_map(), 2, 3)


@pytest.fixture
def subscription_context(container):
    @contextlib.contextmanager
    def setup_subscription_test(prop_name, for_class):
        prop_mock = PropertyMock()
        mover_mock = MagicMock(spec=MoverBase)
        scanner_mock = Mock(spec=ScannerBase)
        target_class = mover_mock \
            if for_class == 'mover_mock' else scanner_mock
        setattr(type(target_class), prop_name, prop_mock)
        handler_mock = Mock()

        with container.mover.override(mover_mock),\
                container.scanner.override(scanner_mock):
            model = container.model()

        prop_mock.assert_not_called()
        yield model, handler_mock
        prop_mock.assert_called_once()
    yield setup_subscription_test


def test_move_call(container):
    scanner_mock = Mock(spec=ScannerBase, **{
        'scan.return_value': (x for x in range(3))
    })
    mover_mock = Mock(spec=MoverBase)
    with container.fs_manipulator.override(Mock(spec=FsManipulatorBase)),\
            container.observable.override(MagicMock(spec=Observable)),\
            container.scanner.override(scanner_mock),\
            container.mover.override(mover_mock):
        model = container.model()

    model.set_dst_folder('dst')
    model.set_src_folder('src')
    model.move()

    scanner_mock.scan.assert_called_once_with('src')
    mover_mock.move.assert_has_calls([call(x, 'dst', False) for x in range(3)])


def test_on_move_finish_subscribe(subscription_context):
    with subscription_context('on_move_finished', 'mover_mock') \
            as (model, handler_mock):
        model.on_move_finished += handler_mock


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
