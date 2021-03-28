# -*- coding: utf-8 -*-

from unittest.mock import call, Mock, MagicMock, PropertyMock

import pytest

from containers import Container
from core.entities.fs import FsManipulatorBase
from core.entities.scanner.base import ScannerBase
from core.entities.mover import MoverBase
from core.types import ScanResult
from core.utils.base import Observable
from utils import full_path
from .fixtures import get_move_map


scanner_result = ScanResult(get_move_map(), 2, 3)


@pytest.fixture
def container():
    ioc = Container()
    yield ioc


class ScannerMock(ScannerBase):

    def scan(self, set_src_folder):
        pass

    @staticmethod
    def get_data():
        return scanner_result


def test_move_call(container):
    scanner_mock = Mock(spec=ScannerBase)
    scanner_mock.get_data.return_value = scanner_result
    mover_mock = Mock(spec=MoverBase)
    with container.fs_manipulator.override(Mock(spec=FsManipulatorBase)),\
            container.observable.override(MagicMock(spec=Observable)),\
            container.scanner.override(scanner_mock),\
            container.mover.override(mover_mock):
        model = container.model()
        model.set_dst_folder('dst')
        model.set_src_folder('src')
        model.move()

    mover_mock.move.assert_called_with(scanner_result, 'dst', False)


def test_on_image_move_prop(container):
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)
    prop_mock = PropertyMock(return_value='')
    mover_mock = MagicMock(spec=MoverBase)
    type(mover_mock).on_image_moved = prop_mock

    with container.mover.override(mover_mock),\
            container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(Mock(return_value=True)):
        model = container.model()
        prop_mock.assert_not_called()
        model.on_image_moved
        prop_mock.assert_called_once()


def test_on_move_finish_report_subscribe(container):
    observable_mock = MagicMock(spec=Observable)
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)
    with container.fs_manipulator.override(fs_manipulator_mock),\
        container.comparator.override(Mock(return_value=True)),\
            container.observable.override(observable_mock):
        model = container.model()
        model.on_move_finished += Mock()

    observable_mock.__iadd__.assert_called_once()


def test_delete_duplicates(container):
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)

    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(Mock(return_value=True)):
        mover = container.mover()
        mover.move(ScanResult(get_move_map(), 2, 3),
                   full_path('tests/out/'), True)

    delete_mock = fs_manipulator_mock.delete
    delete_mock.assert_has_calls([
        call(full_path('tests/data/2.jpg')),
        call(full_path('tests/data/1.jpg'))
    ], any_order=True)

    move_mock = fs_manipulator_mock.move
    move_mock.assert_has_calls([
        call(full_path('tests/data/3.jpg'),
             full_path('tests/out/2017/summer/3.jpg')),
        call(full_path('tests/data/5.jpg'),
             full_path('tests/out/2017/winter (end)/5.jpg')),
        call(full_path('tests/data/4.jpg'),
             full_path('tests/out/2017/winter (end)/4.jpg'))
    ], any_order=True)

    copy_mock = fs_manipulator_mock.copy
    copy_mock.assert_not_called()


def test_clean_mode_safe(container):
    scanner_mock = Mock(spec=ScannerBase)
    mover_mock = Mock(spec=MoverBase)
    with container.mover.override(mover_mock),\
            container.scanner.override(scanner_mock):
        model = container.model()
        model.move()

    mover_mock.move.assert_called_once_with(
        scanner_mock.get_data.return_value, None, False)


def test_clean_mode_dangerously(container):
    scanner_mock = Mock(spec=ScannerBase)
    mover_mock = Mock(spec=MoverBase)
    with container.mover.override(mover_mock),\
            container.scanner.override(scanner_mock):
        model = container.model()
        model.clean_mode(True)
        model.move()

    mover_mock.move.assert_called_once_with(
        scanner_mock.get_data.return_value, None, True)
