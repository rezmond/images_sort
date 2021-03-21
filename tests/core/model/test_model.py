# -*- coding: utf-8 -*-

from unittest.mock import call, patch, Mock, MagicMock

import pytest

from containers import Container
from core.entities.fs import FsManipulatorBase
from core.entities.scanner.base import ScannerBase
from core.entities.mover import Mover, MoverBase
from core.model.model import MoverModel
from core.types import ScanResult
from core.utils.base import Observable
from tests.utils import create_ioc
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


class TestModel:

    def test_move_call(self, container):
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

    def test_on_image_move_prop(self):
        ioc = create_ioc()
        model = MoverModel(ioc, ScannerMock())
        with patch.object(Mover, 'on_image_moved') as patched_prop:
            patched_prop.__get__ = Mock(return_value='')
            patched_prop.__get__.assert_not_called()
            model.on_image_moved
            patched_prop.__get__.assert_called_once()

    def test_on_move_finish_report_subscribe(self):
        ioc = create_ioc()
        observable = MagicMock(spec=Observable)
        ioc.add('observable', observable)
        model = MoverModel(ioc, ScannerMock())

        model.on_move_finished += Mock()

        observable.return_value.__iadd__.assert_called_once()

    def test_delete_duplicates(self, container):
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
