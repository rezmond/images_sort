# -*- coding: utf-8 -*-

from unittest.mock import call, patch, Mock

from ....core.model.model import MoverModel
from ....core.model.mover import Mover
from ....core.model.scanner_base import ScannerBase
from ....core.model.types import ScanResult
from ....utils import full_path
from ...utils import create_ioc
from .fixtures import get_move_map


scanner_result = ScanResult(get_move_map(), 2, 3)


class ScannerMock(ScannerBase):

    def scan(self, set_src_folder):
        pass

    @staticmethod
    def get_data():
        return scanner_result


class TestModel:

    def test_move_call(self):
        ioc = create_ioc()
        model = MoverModel(ioc, ScannerMock())
        model.set_dst_folder('dst')
        model.set_src_folder('src')
        with patch.object(Mover, 'move') as patched_move:
            model.move()

        patched_move.assert_called_with(scanner_result, 'dst', False)

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
        iadd_mock = Mock()
        with patch('images_sort.core.model.mover.Observable') as patched_observable:
            patched_observable.__iadd__ = iadd_mock
            model = MoverModel(ioc, ScannerMock())
            model.on_move_finished += Mock()
        patched_observable.return_value.__iadd__.assert_called_once()

    def test_delete_duplicates(self):
        ioc = create_ioc()
        ioc.add('compare', Mock(return_value=True))
        mover = Mover(ioc)
        # mover.set_dst_folder(full_path('tests/data/'))

        mover.move(ScanResult(get_move_map(), 2, 3),
                   full_path('tests/out/'), True)

        delete_mock = ioc.get('delete')
        delete_mock.assert_has_calls([
            call(full_path('tests/data/2.jpg')),
            call(full_path('tests/data/1.jpg'))
        ], any_order=True)
        move_mock = ioc.get('move')
        move_mock.assert_has_calls([
            call(full_path('tests/data/3.jpg'),
                 full_path('tests/out/2017/summer/3.jpg')),
            call(full_path('tests/data/5.jpg'),
                 full_path('tests/out/2017/winter (end)/5.jpg')),
            call(full_path('tests/data/4.jpg'),
                 full_path('tests/out/2017/winter (end)/4.jpg'))
        ], any_order=True)
        copy_mock = ioc.get('copy')
        copy_mock.assert_not_called()
