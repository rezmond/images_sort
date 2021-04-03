import contextlib
from unittest.mock import call, Mock, MagicMock

import pytest

from containers import Container
from core.types import ScanResult, FileDescriptor
from core.entities.fs import FsManipulatorBase
from core.utils.base import Observable
from utils import full_path


@pytest.fixture
def container():
    ioc = Container()
    yield ioc


@contextlib.contextmanager
def check_subscription(container):
    observable_mock = MagicMock(spec=Observable)
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)

    with container.observable.override(observable_mock),\
            container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(Mock()):
        mover = container.mover()

    handler_mock = Mock()
    yield mover, handler_mock
    observable_mock.__iadd__.assert_called_once_with(handler_mock)


def test_move_without_dst_param(container):
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)
    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(Mock()),\
            pytest.raises(ValueError) as exc_info:
        mover = container.mover()
        mover.move(ScanResult(None, None, None), None)

    assert 'path did not set' in str(exc_info.value), \
        'Should catch not set the src or the dst folder path'


def test_move_by_relative_path(container):
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)

    with container.fs_manipulator.override(fs_manipulator_mock),\
        container.comparator.override(Mock()),\
            pytest.raises(ValueError) as exc_info:
        mover = container.mover()
        mover.move(ScanResult(None, None, None), 'test-1')

    assert 'absolute' in str(exc_info.value), \
        'Should catch not absolute the destination folder path'


def test_move_by_absolute_path(container):
    def comporator_mock(x, _):
        return x.endswith('1.jpg')

    on_item_moved_handler_mock = Mock()
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)

    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(comporator_mock):
        mover = container.mover()
        mover.on_image_moved += on_item_moved_handler_mock

        move_result = mover.move(
            ScanResult({
                '2017': {
                    'spring': [
                        FileDescriptor(full_path('tests/data/2.jpg'), '')
                    ],
                    'summer': [
                        FileDescriptor(full_path('tests/data/3.jpg'), '')
                    ],
                    'winter (end)': [
                        FileDescriptor(full_path('tests/data/5.jpg'), ''),
                        FileDescriptor(full_path('tests/data/4.jpg'), '')
                    ],
                    'winter (begin)': [
                        FileDescriptor(full_path('tests/data/1.jpg'), '')
                    ],
                    'summer': [
                        FileDescriptor(full_path('tests/data/3.jpg'), '')
                    ],
                }
            }, [], []), full_path('tests/out'))

    calls = [
        call(
            full_path('tests/data/2.jpg'),
            full_path('tests/out/2017/spring/2_1.jpg')
        ),
        call(
            full_path('tests/data/5.jpg'),
            full_path('tests/out/2017/winter (end)/5.jpg')
        ),
        call(
            full_path('tests/data/3.jpg'),
            full_path('tests/out/2017/summer/3.jpg')
        ),
        call(
            full_path('tests/data/4.jpg'),
            full_path('tests/out/2017/winter (end)/4.jpg')
        ),
    ]

    copy_mock = fs_manipulator_mock.copy
    copy_mock.assert_has_calls(calls, any_order=True)

    calls = [
        call((
            full_path('tests/data/2.jpg'),
            full_path('tests/out/2017/spring/2_1.jpg')
        )),
        call((
            full_path('tests/data/3.jpg'),
            full_path('tests/out/2017/summer/3.jpg')
        )),
        call((
            full_path('tests/data/5.jpg'),
            full_path('tests/out/2017/winter (end)/5.jpg')
        )),
        call((
            full_path('tests/data/4.jpg'),
            full_path('tests/out/2017/winter (end)/4.jpg')
        )),
    ]
    on_item_moved_handler_mock\
        .assert_has_calls(calls, any_order=True)

    assert move_result == ([
        full_path('tests/data/2.jpg'),
        full_path('tests/data/3.jpg'),
        full_path('tests/data/5.jpg'),
        full_path('tests/data/4.jpg'),
    ], [
        full_path('tests/data/1.jpg'),
    ], [], []), 'Should return correct MoveResult'


def test_on_move_finished_subscribe(container):
    with check_subscription(container) as (mover, handler_mock):
        mover.on_move_finished += handler_mock


def test_on_image_moved_subscribe(container):
    with check_subscription(container) as (mover, handler_mock):
        mover.on_image_moved += handler_mock