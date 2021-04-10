import os
import contextlib
from unittest.mock import call, Mock, MagicMock

import pytest

from core.types import FileWay, MoveType, MoveResult, MoveReport
from core.entities.fs import FsManipulatorBase
from core.utils.base import Observable
from utils import full_path

from_to = (
    (full_path('tests/data/2.jpg'), '2017/spring/'),
    (full_path('tests/data/3.jpg'), '2017/summer/'),
    (full_path('tests/data/5.jpg'), '2017/winter (end)/'),
    (full_path('tests/data/4.jpg'), '2017/winter (end)/'),
    (full_path('tests/data/1.jpg'), '2017/winter (begin)/'),
)


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
        mover.move(FileWay(), '')

    assert 'path did not set' in str(exc_info.value), \
        'Should catch not set the src or the dst folder path'


def test_move_by_relative_path(container):
    fs_manipulator_mock = Mock(spec=FsManipulatorBase)

    with container.fs_manipulator.override(fs_manipulator_mock),\
        container.comparator.override(Mock()),\
            pytest.raises(ValueError) as exc_info:
        mover = container.mover()
        mover.move(FileWay(), 'test-1')

    assert 'absolute' in str(exc_info.value), \
        'Should catch not absolute the destination folder path'


def test_move_by_absolute_path(container):
    def comporator_mock(x, _):
        return x.endswith('/1.jpg')

    def is_file_mock(path):
        return comporator_mock(path, None) or path.endswith('/2.jpg')

    on_item_moved_handler_mock = Mock()
    fs_manipulator_mock = Mock(spec=FsManipulatorBase, **{
        'isfile': is_file_mock
    })

    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(comporator_mock):
        mover = container.mover()
    mover.on_move_finished += on_item_moved_handler_mock

    list(mover.move(
        FileWay(
            src=src,
            dst=dst,
            type=MoveType.MEDIA,
        ), full_path('tests/out')
    ) for (src, dst) in from_to)

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

    on_item_moved_handler_mock.assert_has_calls(
        [
            call(MoveReport(
                result=(
                    MoveResult.ALREADY_EXISTED
                    if comporator_mock(src, None)
                    else MoveResult.MOVED
                ),
                file_way=FileWay(
                    src=src,
                    dst=dst,
                    type=MoveType.MEDIA,
                )
            ))
            for (src, dst) in from_to], any_order=True)


def test_on_move_finished_subscribe(container):
    with check_subscription(container) as (mover, handler_mock):
        mover.on_move_finished += handler_mock


def test_delete_duplicates(container):
    to_delete = from_to[0: 2]
    to_delete_dst = list(map(full_path, (
        os.path.join('tests/out', '2017/spring/2.jpg'),
        os.path.join('tests/out', '2017/summer/3.jpg'),
    )))

    def comporator_mock(_, dst):
        nonlocal to_delete_dst
        return dst in to_delete_dst

    def is_file_mock(path):
        nonlocal to_delete_dst
        return path in to_delete_dst

    fs_manipulator_mock = Mock(spec=FsManipulatorBase, isfile=is_file_mock)

    with container.fs_manipulator.override(fs_manipulator_mock),\
            container.comparator.override(comporator_mock):
        mover = container.mover()

    list(mover.move(
        FileWay(
            src=src,
            dst=dst,
            type=MoveType.MEDIA,
        ), full_path('tests/out'), True
    ) for (src, dst) in from_to)

    delete_mock = fs_manipulator_mock.delete
    delete_mock.assert_has_calls(
        [call(src) for (src, _) in to_delete], any_order=True)

    move_mock = fs_manipulator_mock.move
    expects = [
        call(pair[0], full_path(os.path.join(
            'tests/out', pair[1], os.path.basename(pair[0]))))
        for pair in from_to if pair not in to_delete]
    move_mock.assert_has_calls(expects, any_order=True)

    copy_mock = fs_manipulator_mock.copy
    copy_mock.assert_not_called()
